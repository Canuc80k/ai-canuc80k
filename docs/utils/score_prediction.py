"""Validate a student's CSV/JSON and evaluate against public validation answers."""
from pathlib import Path
import argparse,csv,json,math,re,unicodedata
import numpy as np
from sklearn.metrics import adjusted_rand_score,f1_score
from scipy.stats import wasserstein_distance

def tokens(s):return re.sub(r"[^\w\s]",' ',unicodedata.normalize('NFC',s).lower()).split()
def distance(a,b):
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]
def spans(ends):
    start=0;out=set()
    for i,v in enumerate(ends):
        if v:out.add((start,i+1));start=i+1
    return out
def evaluate(family,answers,predictions):
    if set(answers)!=set(predictions):raise ValueError('Thiếu/thừa ID')
    ids=sorted(answers);y=[answers[i] for i in ids];p=[predictions[i] for i in ids]
    if family=='asr':
        numerator=sum(distance(tokens(a),tokens(b)) for a,b in zip(y,p));denominator=sum(len(tokens(a)) for a in y)
        wer=numerator/denominator;return {'metric':'WER','value':wer,'score':max(0.,1-wer)}
    if family=='translation':
        norm=lambda s:unicodedata.normalize('NFC',s).strip().casefold()
        accuracy=np.mean([norm(a)==norm(b) for a,b in zip(y,p)]);return {'metric':'ExactMatch','value':float(accuracy),'score':float(accuracy)}
    if family=='wordseg':
        scores=[]
        for a,b in zip(y,p):
            if not isinstance(b,list) or len(a)!=len(b) or not b or b[-1]!=1 or any(type(v) is not int or v not in [0,1] for v in b):raise ValueError('Sai ends/length: cần list integer 0/1')
            A,B=spans(a),spans(b);scores.append(2*len(A&B)/(len(A)+len(B)))
        return {'metric':'MeanSpanF1','value':float(np.mean(scores)),'score':float(np.mean(scores))}
    if family in {'prob','lm'}:
        probs=np.asarray(p,dtype=float)
        if probs.ndim!=2 or not np.isfinite(probs).all() or (probs<0).any() or (probs>1).any() or not np.allclose(probs.sum(1),1,atol=1e-6,rtol=0):raise ValueError('Sai probability vector')
        labels=np.asarray(y,dtype=int)
        if labels.max()>=probs.shape[1]:raise ValueError('Thiếu class columns')
        loss=float(-np.log(np.clip(probs[np.arange(len(ids)),labels],1e-12,1)).mean())
        return {'metric':'LogLoss','value':loss,'score':math.exp(-loss)}
    a,b=np.asarray(y,dtype=float),np.asarray(p,dtype=float)
    if a.shape!=b.shape or not np.isfinite(b).all():raise ValueError('Sai shape hoặc NaN/Inf')
    if family=='cluster':
        if not np.equal(b,np.round(b)).all():raise ValueError('Cluster IDs phải integer')
        ari=float(adjusted_rand_score(a,b));return {'metric':'ARI','value':ari,'score':max(0,ari)}
    if family in {'cls','sequence','digits','retrieval','text','tone'}:
        if not np.equal(b,np.round(b)).all():raise ValueError('Label/ID phải integer')
        upper=9 if family in {'digits','retrieval'} else 2
        if (b<0).any() or (b>upper).any():raise ValueError('Label ngoài miền')
        if family in {'text','tone'}:score=float(f1_score(a,b,labels=[0,1,2],average='macro',zero_division=0));metric='MacroF1'
        else:score=float((a==b).mean());metric='Accuracy'
        return {'metric':metric,'value':score,'score':score}
    if family=='mask':
        if not np.isin(b,[0,1]).all():raise ValueError('Mask phải0/1')
        inter=((a==1)&(b==1)).sum(1);union=((a==1)|(b==1)).sum(1)
        score=float(np.where(union>0,inter/np.maximum(1,union),1).mean());return {'metric':'MeanIoU','value':score,'score':score}
    if family=='boxes':
        if b.shape[1]!=4 or (b<0).any() or (b>24).any() or (b[:,0]>b[:,2]).any() or (b[:,1]>b[:,3]).any():raise ValueError('Sai xyxy')
        inter=np.maximum(0,np.minimum(a[:,2],b[:,2])-np.maximum(a[:,0],b[:,0]))*np.maximum(0,np.minimum(a[:,3],b[:,3])-np.maximum(a[:,1],b[:,1]))
        union=(a[:,2]-a[:,0])*(a[:,3]-a[:,1])+(b[:,2]-b[:,0])*(b[:,3]-b[:,1])-inter
        score=float((inter/np.maximum(1e-12,union)).mean());return {'metric':'MeanBoxIoU','value':score,'score':score}
    if family=='gan':
        w=float(wasserstein_distance(a,b));return {'metric':'Wasserstein1D','value':w,'score':math.exp(-w)}
    if family=='audioqa':
        err=float(np.mean(abs(a-b)/np.maximum(abs(a),1e-6)));return {'metric':'RelativeMAE','value':err,'score':math.exp(-err)}
    mse=float(np.mean((a-b)**2));value=mse if family=='noise' else math.sqrt(mse)
    if family in {'mask','denoise'} and ((b<0).any() or (b>1).any()):raise ValueError('Pixel ngoài[0,1]')
    return {'metric':'MSE' if family=='noise' else 'RMSE','value':value,'score':math.exp(-value)}

def read_submission(path,family,header):
    if family=='wordseg':
        def unique_keys(pairs):
            result={}
            for key,value in pairs:
                if key in result:raise ValueError('Trùng ID/key trong JSON')
                result[key]=value
            return result
        with Path(path).open(encoding='utf-8') as f:obj=json.load(f,object_pairs_hook=unique_keys)
        if not isinstance(obj,dict):raise ValueError('JSON phải object')
        return obj
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=header:raise ValueError(f'Header cần {header}, nhận {reader.fieldnames}')
        out={}
        for row in reader:
            if set(row)!=set(header) or any(row[k] is None for k in header):raise ValueError('Sai số cột trong dòng CSV')
            ident=row['id']
            if ident in out:raise ValueError('Trùng ID')
            fields=[row[k] for k in header[1:]]
            if family in {'translation','asr'}:value=fields[0]
            else:
                values=[float(x) for x in fields]
                if any(not math.isfinite(x) for x in values):raise ValueError('NaN/Inf')
                value=values if len(values)>1 else values[0]
            out[ident]=value
        return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--submission',required=True);ap.add_argument('--answers');args=ap.parse_args()
    folder=Path(args.data);meta=json.loads((folder/'DATA_NOTE.json').read_text(encoding='utf-8'))
    answers=json.loads(Path(args.answers or folder/'valid_answers.json').read_text(encoding='utf-8'))
    pred=read_submission(args.submission,meta['family'],meta['output_header'])
    print(json.dumps(evaluate(meta['family'],answers,pred),ensure_ascii=False,indent=2))
