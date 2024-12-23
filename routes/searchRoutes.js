const express = require("express");
const router = express.Router();
const {
  searchMediInfo,
  getMediInfo,
  searchMediInfoById,
} = require("../controllers/getMediInfoCtrl");

router.get("/search", searchMediInfo);
router.get("/info", getMediInfo);
router.get("/info/:id", searchMediInfoById);

module.exports = router;
