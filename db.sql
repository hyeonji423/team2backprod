CREATE TABLE users (
    id SERIAL PRIMARY KEY,            -- 자동 증가하는 기본 키
    email VARCHAR(100) UNIQUE NOT NULL,        -- 이메일 (고유 값)
    password VARCHAR(255) NOT NULL,   -- 비밀번호 (bcrypt 사용 예정)
    birth_date DATE NOT NULL,         -- 생년월일
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 생성 날짜
);

CREATE TABLE mymedicine (
    id SERIAL PRIMARY KEY,            -- 자동 증가하는 기본 키
    medi_name VARCHAR(255) NOT NULL,   -- 약품 이름
    company_name VARCHAR(255),         -- 회사 이름 (NULL 가능)
    buying_date DATE,                  -- 구매 날짜 (NULL 가능)
    exp_date DATE NOT NULL,             -- 유효기간 (년 단위)
    main_symptom VARCHAR(255),         -- 주요 증상 (NULL 가능)
    memo TEXT,                         -- 메모 (NULL 가능)
    notification BOOLEAN,             -- 알림 여부
    user_id INT,                       -- 사용자 ID (외래 키로 사용)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)  -- 사용자 ID 외래 키
);

-- 알림 여부 추가
ALTER TABLE mymedicine
ADD COLUMN notification BOOLEAN;

-- date 한국시간대로 변경
ALTER TABLE mymedicine 
ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE,
ALTER COLUMN created_at SET DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Seoul');

-- 알림설정에 필요한 데이터 선택
SELECT 
    m.id AS mediId,
    m.medi_name AS mediName,
    m.exp_date AS expDate,
    u.email AS userEmail
FROM 
    mymedicine m
JOIN 
    users u ON m.user_id = u.id
WHERE 
    m.exp_date::date = CURRENT_DATE + INTERVAL '7 days'
    AND m.notification = true;

-- 알림 발송 기록 테이블 생성
CREATE TABLE notification_logs (
    id SERIAL PRIMARY KEY,                    -- 로그 고유 ID
    medicine_id INTEGER NOT NULL,             -- 약품 ID
    sent_date TIMESTAMP WITH TIME ZONE        -- 발송 시간 (한국 시간)
        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Seoul'),
    status VARCHAR(50) NOT NULL CHECK (status IN ('sent', 'failed')),
    error_message TEXT,                       -- 실패 시 에러 메시지
    created_at TIMESTAMP WITH TIME ZONE       -- 로그 생성 시간
        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Seoul'),
    CONSTRAINT fk_medicine_id 
        FOREIGN KEY (medicine_id) 
        REFERENCES mymedicine(id)
        ON DELETE CASCADE                     -- 약품이 삭제되면 로그도 삭제
);

-- 시스템 에러 로그를 기록하는 테이블
CREATE TABLE error_logs (
    id SERIAL PRIMARY KEY,                    -- 에러 로그 고유 ID
    error_message TEXT NOT NULL,              -- 에러 메시지
    error_date TIMESTAMP WITH TIME ZONE       -- 에러 발생 시간
        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Seoul'),
    stack_trace TEXT,                         -- 스택 트레이스 (선택사항)
    created_at TIMESTAMP WITH TIME ZONE       -- 로그 생성 시간
        DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Seoul')
);

-- 로그 조회를 위한 인덱스 생성
CREATE INDEX idx_notification_logs_medicine_id ON notification_logs(medicine_id);
CREATE INDEX idx_notification_logs_sent_date ON notification_logs(sent_date);
CREATE INDEX idx_notification_logs_status ON notification_logs(status);
CREATE INDEX idx_error_logs_error_date ON error_logs(error_date);

-- 특정 약품의 알림 발송 이력 조회
SELECT * FROM notification_logs 
WHERE medicine_id = :medicine_id 
ORDER BY sent_date DESC;

-- 실패한 알림 목록 조회
SELECT * FROM notification_logs 
WHERE status = 'failed' 
ORDER BY sent_date DESC;

-- 최근 시스템 에러 조회
SELECT * FROM error_logs 
ORDER BY error_date DESC 
LIMIT 10;