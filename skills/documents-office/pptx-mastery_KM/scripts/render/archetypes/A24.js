module.exports = function createA24Handler(renderers) {
  return function handleA24(ctx) {
    return renderers.renderA24QaClosing(ctx);
  };
};
