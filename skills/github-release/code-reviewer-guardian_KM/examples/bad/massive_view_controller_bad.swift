
import UIKit

class UserProfileViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    private let tableView = UITableView()
    private var users: [String] = []
    private let url = URL(string: "http://example.com/users")! // ATS risk (http)
    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(tableView)
        tableView.frame = view.bounds
        tableView.dataSource = self
        tableView.delegate = self

        // Networking in VC
        let task = URLSession.shared.dataTask(with: url) { data, _, _ in
            guard let data = data, let list = try? JSONDecoder().decode([String].self, from: data) else { return }
            self.users = list // retains VC strongly in closure
            DispatchQueue.main.sync { // risk of deadlock if called on main
                self.tableView.reloadData()
            }
        }
        task.resume()
    }

    // Long method
    func computeStatisticsForUsers(_ input: [String]) -> [String: Int] {
        var result: [String: Int] = [:]
        for name in input {
            let count = name.filter { $0.isLetter }.count
            if let old = result["letters"] {
                result["letters"] = old + count
            } else {
                result["letters"] = count
            }
            // ... (pretend 100 lines of logic) ...
            if name.contains("admin") {
                print("debug admin") // debug print in prod
            }
        }
        return result
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int { users.count }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = UITableViewCell(style: .subtitle, reuseIdentifier: "cell")
        cell.textLabel?.text = users[indexPath.row]
        return cell
    }
}
