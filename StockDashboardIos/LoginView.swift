import SwiftUI
struct LoginView: View {
    @State private var username = ""
    @State private var password = ""
    @State private var loginMessage = ""
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
            case 401:
                loginMessage = "账号或密码错误"
            default:
                loginMessage = "登录失败"
            }
        } catch {
            loginMessage = "登陆请求失败：\(error.localizedDescription)"
        }}
            
            
            
        
            
    var body: some View {
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
#Preview {
    LoginView()
}
            
