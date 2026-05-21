module.exports = function createA20Handler(renderers) {
  return function handleA20(ctx) {
    return renderers.renderA20BeforeAfter(ctx);
  };
};
