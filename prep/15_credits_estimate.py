import math
P={'deepseek-v4-flash':(0.04444,0.13332),'glm-53-flash':(0.15,0.50),'qwen3.5-397b':(0.55,3.50),
   'gemma-4-31b-it':(0.09,0.34),'gemma-4-26b-a4b-it':(0.0765,0.255),'qwen3.8-27b':(0.039,1.25),'glm-5.2':(0.104,4.40)}
H=list(P)
print('cost per 100k calls (2500 in / 100 out, no reasoning) and with +400 reasoning:')
for m,(i,o) in P.items():
    print(f'  {m:22s} ${100000*(2500*i+100*o)/1e6:7.2f}   ${100000*(2500*i+500*o)/1e6:7.2f}')
def build(core, intok, mon_in, mon_models, n=20, conf_scale=1.0, qwen_only_main=True):
    rows=[]
    def add(name,models,Ns,var,nep,inn,rounds=30,mult=None):
        mult=len(models) if mult is None else mult
        rows.append((name,models,sum(N*rounds for N in Ns)*var*nep*mult,inn))
    add('main grid',H,[5,10,20],1,n,intok)
    add('prompt abl',core,[5,10,20],2,n,intok)
    add('Q1 abl',core,[10],5,n,intok)
    add('Q3',core,[10],7,n,intok)
    add('Q4',core,[10],8,n,intok)
    add('Q5/6 monitors',mon_models,[1],1,600,mon_in,rounds=160,mult=1)
    add('Q7',core[:2],[5],27,n,intok,rounds=10)
    five=sum(r[2] for r in rows[:5])/5
    rows.append(('confirm',core,2*five*conf_scale,intok))
    return rows
def cost(rows,out,reason,retry=1.15):
    t=0
    for name,ms,c,inn in rows:
        ci=sum(P[m][0] for m in ms)/len(ms); co=sum(P[m][1] for m in ms)/len(ms)
        t+=c*(inn*ci+(out+reason)*co)/1e6
    return t*retry, sum(r[2] for r in rows)
core3=['deepseek-v4-flash','qwen3.5-397b','gemma-4-31b-it']
core2=['deepseek-v4-flash','gemma-4-31b-it']
sc={
 'A as written (2500 in, 3 core, monitors 6k on core3)':build(core3,2500,6000,core3),
 'B history window (1200 in), monitors 3k':build(core3,1200,3000,core3),
 'C = B + ablations/confirm on 2 cheap models, monitors on deepseek only':build(core2,1200,3000,['deepseek-v4-flash']),
}
for k,r in sc.items():
    for lab,rs in (('no reasoning',0),('+400 reasoning',400)):
        c,n=cost(r,100,rs); print(f'{k} | {lab}: ${c:,.0f} for {n:,.0f} calls')
# scaling episodes for C
r=build(core2,1200,3000,['deepseek-v4-flash'],n=20)
for nn in (20,40,50,100):
    r=build(core2,1200,3000,['deepseek-v4-flash'],n=nn)
    c0,n0=cost(r,100,0); c4,_=cost(r,100,400); print(f'C with n={nn}/cell: ${c0:,.0f} (no reasoning) ${c4:,.0f} (+400 reasoning), {n0:,.0f} calls, {n0/16/3600:.1f} h at 16 calls/s')
# depth 60 rounds
r=build(core2,1200,3000,['deepseek-v4-flash'],n=20)
c,n=cost(r,100,0); print('C at 60 rounds (calls x2, window same):',round(2*c))
