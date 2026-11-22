//
//  StockDeatilView.swift
//  StockDashboardIos
//
//  Created by 1125 on 2026/11/22.
//

import SwiftUI

struct StockDeatilView: View {
    let symbol : String
    let initialQuote : StockImformation?
    var body: some View {
        Form{
            Text("股票代码\(symbol)")
            if let stockInfo = initialQuote{
                Text("股票价格\(stockInfo.price ?? "N/A")")
                if let rawTime = stockInfo.trade_time,
                   let tradeDate = try? Date(rawTime, strategy: .iso8601){
                    Text("成交时间\(tradeDate.formatted(date: .numeric, time: .standard))")}
                else{
                    Text("成交时间N/A")
                }
                
                Text("昨日收盘价\(stockInfo.previous_close ?? "N/A")")
                switch stockInfo.market_data_type{
                case 1:
                    Text("实时行情")
                case 2:
                    Text("冻结行情")
                case 3:
                    Text("延迟行情")
                case 4:
                    Text("延迟冻结行情")
                default:
                    Text("未知行情类型")
                }
            }
        }
    }
}

#Preview {StockDeatilView(symbol: "AAPL", initialQuote: StockImformation(symbol: "AAPL", price: "150.00", trade_time: "2023-11-22T14:30:00Z", previous_close: "148.00", market_data_type: 1))}
