import SwiftUI
import MapKit

struct MapBridge: UIViewRepresentable {
    typealias UIViewType = MKMapView

    @Binding var region: MKCoordinateRegion
    var annotations: [MKPointAnnotation] = []

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> MKMapView {
        let map = MKMapView(frame: .zero)
        map.delegate = context.coordinator
        map.setRegion(region, animated: false)

        // Example gesture recognizer: long press to drop pin
        let longPress = UILongPressGestureRecognizer(target: context.coordinator, action: #selector(Coordinator.handleLongPress(_:)))
        map.addGestureRecognizer(longPress)
        return map
    }

    func updateUIView(_ uiView: MKMapView, context: Context) {
        context.coordinator.parent = self
        if uiView.region.center.latitude != region.center.latitude ||
           uiView.region.center.longitude != region.center.longitude ||
           uiView.region.span.latitudeDelta != region.span.latitudeDelta ||
           uiView.region.span.longitudeDelta != region.span.longitudeDelta {
            uiView.setRegion(region, animated: true)
        }
        uiView.removeAnnotations(uiView.annotations)
        uiView.addAnnotations(annotations)
    }

    static func dismantleUIView(_ uiView: MKMapView, coordinator: Coordinator) {
        uiView.delegate = nil
        uiView.gestureRecognizers?.forEach { uiView.removeGestureRecognizer($0) }
    }

    final class Coordinator: NSObject, MKMapViewDelegate {
        weak var map: MKMapView?
        var parent: MapBridge

        init(_ parent: MapBridge) { self.parent = parent }

        @objc func handleLongPress(_ gesture: UILongPressGestureRecognizer) {
            guard let map = gesture.view as? MKMapView else { return }
            let point = gesture.location(in: map)
            let coord = map.convert(point, toCoordinateFrom: map)
            let pin = MKPointAnnotation()
            pin.coordinate = coord
            map.addAnnotation(pin)
        }

        func mapView(_ mapView: MKMapView, regionDidChangeAnimated animated: Bool) {
            self.map = mapView
            // Push region change back to SwiftUI (avoid feedback loops by writing conditionally)
            if parent.region.center.latitude != mapView.region.center.latitude {
                parent.region = mapView.region
            }
        }
    }
}
