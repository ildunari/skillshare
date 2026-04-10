module.exports = function createA05Handler(renderers) {
  return function handleA05(ctx) {
    return renderers.renderA5Split5050(ctx);
  };
};
