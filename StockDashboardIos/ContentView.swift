import SwiftUI
import Playgrounds
import Foundation
struct PaperAccount : Decodable {
    let account_id : String
    let netvalue : String
    let as_of : String
    let currency : String
    let source : String
    let daily_pnl : String
    let realized_pnl : String
    let cash : String?
    let buying_power : String?
    let stock_market_value : String?
    let unrealized_pnl : String?
    let holding : [PaperPosition]
}

struct PaperPosition : Decodable {
    let symbol : String
    let quantity : String
    let average_cost : String
    let currency : String
    let market_price : String
    let market_value : String
    let unrealized_pnl : String
    let realized_pnl : String
    let daily_pnl : String?}

struct PaperAccountResponse : Decodable {
    let account : PaperAccount?
}
struct ContentView: View {
    @State private var paperAccount : PaperAccount?
    @State private var selectedQuote : StockImformation?
    func refreshAccount()async{
        guard let url = URL(string:"https://dzp1125.me/accounts/paper") else {return}
        
        do{
            let (data,respone) = try await URLSession.shared.data(from: url)
            print((respone as? HTTPURLResponse)?.statusCode ?? 0,data.count)
            let reply = try JSONDecoder().decode(PaperAccountResponse.self, from: data)
            guard let account = reply.account else {return}
            paperAccount = account
               }
        catch{
            print(error)}}
    var body: some View{
        ScrollView{
            VStack(alignment: .leading, spacing: 8){
                Text("模拟盘账号")
                if let account = paperAccount{
                    Text("账号\(account.account_id)")
                    Text("更新时间\(account.as_of)")
                    Text("股票市值\(account.stock_market_value ?? "N/A")")
                    Text("净值\(account.netvalue)")
                    Text("货币\(account.currency)")
                    Text("日盈亏\(account.daily_pnl)")
                    Text("已实现盈亏\(account.realized_pnl)")
                    Text("未实现盈亏\(account.unrealized_pnl ?? "N/A")")
                    Text("现金\(account.cash ?? "N/A")")
                    Text("购买力\(account.buying_power ?? "N/A")")
                    Text("数据来源\(paperAccount?.source ?? "N/A")")
                    
                    Text("持仓信息")
                    HStack (alignment: .top){
                    Grid(alignment: .leading) {
                    ForEach(account.holding, id: \.symbol) { position in
                        Button(position.symbol) {
                            Task{
                                selectedQuote = await searchStock(symbol: position.symbol)
                            }
                        }
                        .buttonStyle(.plain)
                        }
                    }
                        ScrollView(.horizontal) {
                            Grid(alignment: .leading) {
                                ForEach(account.holding, id: \.symbol) { position in
                                    GridRow {
                                        Text("价格\(position.market_price)")
                                        Text("持仓数量\(position.quantity)")
                                        Text("平均成本\(position.average_cost)")
                                        Text("货币\(position.currency)")
                                        Text("市场价值\(position.market_value)")
                                        Text("未实现盈亏\(position.unrealized_pnl)")
                                        Text("已实现盈亏\(position.realized_pnl)")
                                        Text("日盈亏\(position.daily_pnl ?? "N/A")")
                                    }
                                }
                            }
                        }
                    }
                } else {
                    Text("未获取到账户信息")
                }
                Button("刷新") { Task { await refreshAccount() } }
            }.task { await refreshAccount() }
            
            
            
                    .padding()}.navigationDestination(item: $selectedQuote) { quote in
                        StockDeatilView(symbol: quote.symbol,initialQuote: quote)}
                        
    }
    }

#Preview {
    NavigationStack{
        
        ContentView()}
}

#Playground {
    let json = """
    {
        "netvalue": "10000.00",
        "as_of": "17:09:47"
    }
    """
    print("json: \(json)")
    let data = Data(json.utf8)
    print(data.count)
    do{
        let account = try
        JSONDecoder().decode(PaperAccount.self, from: data)
        print(account.netvalue)
        print(account.as_of)
    }catch{print(error)
        
    }
}
