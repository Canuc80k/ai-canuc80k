# -*- coding: utf-8 -*-

# Edit distance theo từ để tính WER; minh họa scoring, không ASR model.
reference="go to school".split(); hypothesis="go school".split()
dp=[[0]*(len(hypothesis)+1) for _ in range(len(reference)+1)]
for i in range(len(reference)+1): dp[i][0]=i
for j in range(len(hypothesis)+1): dp[0][j]=j
for i in range(1,len(reference)+1):
    for j in range(1,len(hypothesis)+1):
        dp[i][j]=min(dp[i-1][j]+1,dp[i][j-1]+1,
                     dp[i-1][j-1]+(reference[i-1]!=hypothesis[j-1]))
edits=dp[-1][-1]
print("Ref:",reference,"Hyp:",hypothesis)
print("Edits:",edits,"WER:",round(edits/len(reference),6))
assert edits==1
# asr_demo.py có code Whisper cho audio/checkpoint được cấp, không giả transcript từ fixture.
