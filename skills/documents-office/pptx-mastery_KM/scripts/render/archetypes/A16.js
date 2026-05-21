module.exports = function createA16Handler(renderers) {
  return function handleA16(ctx) {
    return renderers.renderA16ArchitectureDiagram(ctx);
  };
};
