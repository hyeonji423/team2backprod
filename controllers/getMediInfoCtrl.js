const database = require("../database/database");

exports.searchMediInfo = async (request, response) => {
  let { term } = request.query;
  // "약" 글자가 끝에 있으면 제거
  term = term.endsWith('약') ? term.slice(0, -1) : term;
  
  try {
    const results = await database.pool.query(
      "SELECT * FROM medi_info WHERE 효능 LIKE $1 OR 제품명 LIKE $1 OR 주성분 LIKE $1 LIMIT 20",
      [`%${term}%`]
    );
    return response.status(200).json(results.rows);
  } catch (error) {
    console.error("검색 오류:", error);
    return response.status(500).json({ message: "서버 오류가 발생했습니다." });
  }
};

exports.getMediInfo = async (request, response) => {
  try {
    const results = await database.pool.query("SELECT * FROM medi_info ORDER BY 아이디 ASC LIMIT 50");

    return response.status(200).json(results.rows);
  } catch (error) {
    console.error("데이터베이스 오류 상세:", error);
    return response.status(500).json({
      message: "서버 오류가 발생했습니다.",
      error: error.message,
    });
  }
};

exports.searchMediInfoById = async (request, response) => {
  const { id } = request.params;  // request.query 에서 변경
  try {
    const results = await database.pool.query(
      "SELECT * FROM medi_info WHERE 아이디 = $1",  // id 에서 변경
      [id]
    );

    if (results.rows.length === 0) {
      return response.status(404).json({ message: "약품을 찾을 수 없습니다." });
    }

    return response.status(200).json(results.rows[0]);  // 단일 객체로 반환
  } catch (error) {
    console.error("검색 오류:", error);
    return response.status(500).json({ message: "서버 오류가 발생했습니다." });
  }
};
