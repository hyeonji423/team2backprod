const router = require("express").Router();
const { emailCtrl, notificationCtrl } = require("../controllers/emailCtrl");

router.post('/send-email', emailCtrl );
// router.post('/notifications', notificationCtrl );

module.exports = router;
