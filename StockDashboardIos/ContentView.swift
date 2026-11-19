import SwiftUI
import Playgrounds
import Foundation
struct PaperAccount : Decodable {
    let netvalue : String
    let as_of : String
}
    

struct ContentView: View {
    @State private var netvalue = "10000.00"
    @State private var updatedAt = "17:09:47"
    func refreshAccount(){let json = """
                {
                    "netvalue": "10222.00",
                    "as_of": "17:10:00"
                }
                """
        let data = Data(json.utf8)
        do{
            let account = try JSONDecoder().decode(PaperAccount.self, from: data)
            updatedAt = account.as_of
            netvalue = account.netvalue
        }
        catch{
            print(error)}}
    var body: some View{
        VStack(alignment: .leading, spacing: 8){
            Text("更新时间 \(updatedAt)")
            Text("模拟盘账号")
            Text("账户净值\(netvalue)usd")
            Button("刷新") {refreshAccount()}
        }
        
        
        
        .padding()}
    }

#Preview {
    ContentView()
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
