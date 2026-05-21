module.exports = function createA07Handler(renderers) {
  return function handleA07(ctx) {
    return renderers.renderA7BigNumberCallout(ctx);
  };
};
