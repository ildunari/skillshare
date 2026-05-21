module.exports = function createA01Handler(renderers) {
  return function handleA01(ctx) {
    return renderers.renderA1Cover(ctx);
  };
};
