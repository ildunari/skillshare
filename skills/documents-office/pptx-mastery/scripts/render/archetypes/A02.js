module.exports = function createA02Handler(renderers) {
  return function handleA02(ctx) {
    return renderers.renderA2SectionDivider(ctx);
  };
};
