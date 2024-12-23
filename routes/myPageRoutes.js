const router = require("express").Router();
const { getMyMedi } = require("../controllers/getMyMediCtrl");
const { postMyMedi } = require("../controllers/postMyMediCtrl");
const { deleteMyMedi } = require("../controllers/deleteMyMediCtrl");
const { updateMyMedi } = require("../controllers/updateMyMediCtrl");

router.post("/post_myMedi", postMyMedi);
router.get("/get_myMediList/:user_id", getMyMedi); // :user_id는 다이나믹한 문자열의 이름을 지정
router.delete("/delete_myMediList/:medicine_id", deleteMyMedi);
router.put("/update_myMediList/:medicine_id", updateMyMedi);

module.exports = router;
