
import UIKit
import Combine

protocol UserService {
    func loadUsers() async throws -> [String]
}

final class URLSessionUserService: UserService {
    func loadUsers() async throws -> [String] {
        let (data, _) = try await URLSession.shared.data(from: URL(string: "https://example.com/users")!)
        return try JSONDecoder().decode([String].self, from: data)
    }
}

final class UserListViewModel: ObservableObject {
    @Published private(set) var users: [String] = []
    private let service: UserService

    init(service: UserService) { self.service = service }

    @MainActor
    func refresh() async {
        do { users = try await service.loadUsers() }
        catch { users = []; /* surface error */ }
    }
}

final class UserProfileViewController: UIViewController {
    private let vm: UserListViewModel
    private var bag = Set<AnyCancellable>()
    private let tableView = UITableView()

    init(vm: UserListViewModel) { self.vm = vm; super.init(nibName: nil, bundle: nil) }
    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.frame = view.bounds
        view.addSubview(tableView)
        vm.$users.receive(on: RunLoop.main).sink { [weak self] _ in
            self?.tableView.reloadData()
        }.store(in: &bag)
        Task { await vm.refresh() }
    }
}
