// Metal shader inspiration only.
// Keep this separate from the default Liquid Glass implementation. Use native
// glassEffect APIs for controls and only add shaders to isolated decorative
// backgrounds or previews after accessibility and performance review.

/*
#include <metal_stdlib>
using namespace metal;

struct GlassUniforms {
    float2 size;
    float time;
    float intensity;
};

fragment half4 subtleGlare(float2 position [[position]],
                           constant GlassUniforms &uniforms [[buffer(0)]]) {
    float2 uv = position / uniforms.size;
    float diagonal = smoothstep(0.46, 0.50, uv.x + uv.y + sin(uniforms.time) * 0.08)
                   - smoothstep(0.52, 0.58, uv.x + uv.y + sin(uniforms.time) * 0.08);
    float edge = smoothstep(0.0, 0.08, uv.x) * smoothstep(1.0, 0.92, uv.x);
    return half4(half3(diagonal * edge * uniforms.intensity), half(diagonal * 0.22));
}
*/

// SwiftUI usage pattern after adding a real .metal file to the app target:
// view.layerEffect(ShaderLibrary.subtleGlare(.float2(size), .float(time), .float(0.4)), maxSampleOffset: .zero)
// Disable this under Reduce Motion, Low Power Mode, or when the view is offscreen.
