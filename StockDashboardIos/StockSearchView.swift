

import SwiftUI
struct StockImformation: Decodable,Hashable{
    let symbol : String
    let price : String?
    let trade_time : String?
    let previous_close : String?
    let market_data_type : Int
}
func searchStock(symbol: String ) async -> StockImformation?{
    guard let url = URL(string: "https://dzp1125.me/stock/\(symbol)/search") else {return nil}
    do{
        let (data,response) = try await URLSession.shared.data(from: url)
        print((response as? HTTPURLResponse)?.statusCode ?? 0,data.count)
        let reply = try JSONDecoder().decode(StockImformation.self, from: data)
        return reply
        
        
    }
    catch{
        print(error)
        return nil}}

    
struct StockSearchView: View {
    @State private var stockCode = ""
    @State private var stockInfo : StockImformation?
    

    var body: some View {
        NavigationStack{
            Form {
                Text("股票搜索")
                TextField("股票代码",text : $stockCode)
                Button("搜索") {
                    Task{
                        stockInfo = await searchStock(symbol: stockCode)
                    }
                }
                if let stockInfo = stockInfo{
                    let price = Double(stockInfo.price ?? "")
                    let previousClose = Double(stockInfo.previous_close ?? "")
                    
                    NavigationLink{
                        StockDeatilView(symbol: stockInfo.symbol, initialQuote: stockInfo)
                    } label: {
                        LabeledContent("\(stockInfo.symbol)  \(stockInfo.price ?? "暂无价格")") {
                            if let price = price, let previousClose = previousClose, previousClose != 0 {let changePercent = (price - previousClose) / previousClose * 100
                                Text(String(format: "%.2f%%", changePercent))
                                
                                }
                            
                            else{
                                Text("-")}
                            
                        }
                    }
                    
                }
            
                else{
                    Text("未获取到股票信息")
                }
            }
        }
            
    }
}

#Preview {
    StockSearchView()
}
