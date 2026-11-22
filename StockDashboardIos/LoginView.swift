import SwiftUI
struct LoginView: View {
    @State private var username = ""
    @State private var password = ""
    @State private var loginMessage = ""
    @State private var isLoggedIn = false
    @State private var isCheckingLoginStatus = true
    func check_in() async {
        guard let url = URL(string: "https://dzp1125.me/accounts/me") else {return}
        do {
            let (_,response) = try await URLSession.shared.data(from: url)
            let status = (response as? HTTPURLResponse)?.statusCode
            switch status{
            case 200:
                isLoggedIn = true
            case 401:
                isLoggedIn = false
            default:
                isLoggedIn = false
                loginMessage = "服务器响应异常，占时无法检查登录状态"
            }
        } catch {
            loginMessage = "无法连接服务器，请检查网络连接"
            print("检查登录状态失败：\(error.localizedDescription)")
        }}
    
    func login() async {
        loginMessage = "正在登录..."
        guard let url = URL(string: "https://dzp1125.me/accounts/login") else {loginMessage = "无效的URL"
            return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let fields = ["account_id": username,"password":password]
        do {
            request.httpBody = try JSONEncoder().encode(fields)
            let (_, response) = try await URLSession.shared.data(for: request)
            let status = (response as? HTTPURLResponse)?.statusCode
            switch status{
            case 200:
                loginMessage = "登录成功"
                isLoggedIn = true
            case 401:
                loginMessage = "账号或密码错误"
            default:
                loginMessage = "登录失败"
            }
        } catch {
            loginMessage = "登陆请求失败：\(error.localizedDescription)"
        }}
    
    
    
    
    
    var body: some View {
        if isCheckingLoginStatus {
            ProgressView("正在检查登录状态...")
                .task {
                    await check_in()
                    isCheckingLoginStatus = false
                }
        } else if isLoggedIn {
            TabView{
                Tab("账户", systemImage: "list.bullet") {NavigationStack{
                    ContentView()}
                }
                Tab("搜索", systemImage: "magnifyingglass") {
                    StockSearchView()
                }
                
            }
        } else {
            
            Form {
                Text("账户登录")
                TextField("账号",text: $username)
                SecureField("密码",text: $password)
                Button("登录") {Task{await login()}
                }
                Text(loginMessage)
                
            }
        }
    }
}
#Preview {
    LoginView()
}
            
