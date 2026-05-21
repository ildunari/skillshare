module.exports = function createA03Handler(renderers) {
  return function handleA03(ctx) {
    return renderers.renderA3Agenda(ctx);
  };
};
