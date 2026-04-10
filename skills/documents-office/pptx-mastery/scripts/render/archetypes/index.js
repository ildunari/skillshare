const A01 = require("./A01");
const A02 = require("./A02");
const A03 = require("./A03");
const A04 = require("./A04");
const A05 = require("./A05");
const A06 = require("./A06");
const A07 = require("./A07");
const A08 = require("./A08");
const A09 = require("./A09");
const A10 = require("./A10");
const A11 = require("./A11");
const A12 = require("./A12");
const A13 = require("./A13");
const A14 = require("./A14");
const A15 = require("./A15");
const A16 = require("./A16");
const A17 = require("./A17");
const A18 = require("./A18");
const A19 = require("./A19");
const A20 = require("./A20");
const A21 = require("./A21");
const A22 = require("./A22");
const A23 = require("./A23");
const A24 = require("./A24");

module.exports = function createArchetypeHandlers(renderers) {
  return {
    A1: A01(renderers),
    A2: A02(renderers),
    A3: A03(renderers),
    A4: A04(renderers),
    A5: A05(renderers),
    A6: A06(renderers),
    A7: A07(renderers),
    A8: A08(renderers),
    A9: A09(renderers),
    A10: A10(renderers),
    A11: A11(renderers),
    A12: A12(renderers),
    A13: A13(renderers),
    A14: A14(renderers),
    A15: A15(renderers),
    A16: A16(renderers),
    A17: A17(renderers),
    A18: A18(renderers),
    A19: A19(renderers),
    A20: A20(renderers),
    A21: A21(renderers),
    A22: A22(renderers),
    A23: A23(renderers),
    A24: A24(renderers),
  };
};
