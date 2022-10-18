from absbox.local.china import 信贷ABS

# 分润模式
test03 = 信贷ABS(
    "Split the residual"
    ,{"封包日":"2021-03-01","起息日":"2021-10-15","首次兑付日":"2021-11-26"
      ,"法定到期日":"2060-12-01","收款频率":"月末","付款频率":["每月",26]}       
    ,{'清单':[["按揭贷款"
        ,{"放款金额":120,"放款利率":["浮动",0.085,{"基准":"LPR5Y","利差":0.01,"重置频率":"每月"}],"初始期限":30
          ,"频率":"每月","类型":"等额本金","放款日":"2020-06-01"}
          ,{"当前余额":180
          ,"当前利率":0.08
          ,"剩余期限":10
          ,"状态":"正常"}]]
     }
    ,(("账户01",{"余额":0}),)
    ,(("A1",{"当前余额":100
             ,"当前利率":0.07
             ,"初始余额":100
             ,"初始利率":0.07
             ,"起息日":"2020-01-03"
             ,"利率":{"固定":0.08}
             ,"债券类型":{"过手摊还":None}
             })
      ,("B",{"当前余额":20
             ,"当前利率":0.0
             ,"初始余额":100
             ,"初始利率":0.07
             ,"起息日":"2020-01-03"
             ,"利率":{"固定":0.00}
             ,"债券类型":{"权益":None}
             }))
    ,(("服务商费用",{"类型":{"固定费用":25}}),)
    ,{"未违约":[
         ["支付利息","账户01",["A1"]]
         ,["支付本金","账户01",["A1"]]
         ,["支付本金","账户01",["B"]]
         ,["支付收益","账户01","B"]
      ]
     ,"回款后":[]
     ,"清仓回购":[["出售资产",["正常|违约",1.0,0.0],"账户01"]
                ,["支付费用收益","账户01","服务商费用",{"余额百分比":0.7}]
                ,["支付收益","账户01","B"]]}
    ,(["利息回款","账户01"]
      ,["本金回款","账户01"]
      ,["早偿回款","账户01"]
      ,["回收回款","账户01"])
    ,None
    ,None
)

# 需要配合 清仓回购 假设触发清仓，才能执行分润动作。

myAssumption = [{"CPR":0.00}
                ,{"回收":(0.5,1)}
                ,{"CDR":0.00}
                ,{"清仓":[{"指定日之后":"2021-11-28"}]}
                ,{"利率":["LPR5Y",[["2022-01-01",0.05],["2022-08-01",0.05],["2023-08-01",0.06]]]}
               ]
