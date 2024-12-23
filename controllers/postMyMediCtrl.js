const database = require("../database/database");
const path = require("path");
const ROOT_PATH = "http://localhost:8000";

exports.postMyMedi = async (request, response) => {
  try {
    let {
      mediName,
      companyName,
      mainSymptom,
      expDate,
      buyingDate,
      memo,
      user_id,
      notification,
    } = request.body;

    // 필수 입력값 검증
    if (!mediName || !expDate || !user_id) {
      return response.status(400).json({
        msg: "필수 입력값이 누락되었습니다. (제품명, 유효기간, 사용자 ID는 필수입니다)",
      });
    }

    // 한국 시간(KST)으로 변환하는 함수
    const convertToKST = (date) => {
      const koreaTime = new Date(date + "T00:00:00+09:00");
      return koreaTime.toISOString().split("T")[0]; // 날짜만 반환 (yyyy-mm-dd)
    };

    // `buyingDate`와 `expDate`를 한국 시간으로 변환
    const sanitizedBuyingDate = buyingDate ? convertToKST(buyingDate) : null;
    const sanitizedExpDate = convertToKST(expDate);

    const sanitizedData = [
      mediName,
      companyName || null,
      sanitizedBuyingDate, // 변환된 한국 시간 구매 날짜
      sanitizedExpDate,
      mainSymptom || null,
      memo || null,
      user_id,
      notification,
    ];

    await database.pool.query(
      "INSERT INTO mymedicine (medi_name, company_name, buying_date, exp_date, main_symptom, memo, user_id, notification) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
      sanitizedData
    );

    return response
      .status(201)
      .json({ msg: "약품이 성공적으로 등록되었습니다." });
  } catch (error) {
    return response.status(500).json({ msg: "약품정보 입력 오류: " + error });
  }
};
