// examples/before_after_gcd_to_async.swift
// BEFORE
DispatchQueue.global().async {
    let a = heavyWork()
    DispatchQueue.main.async { updateUI(a) }
}
// AFTER
@MainActor
func updateUIAsync() async {
    let a = await Task.detached { heavyWork() }.value
    updateUI(a)
}
