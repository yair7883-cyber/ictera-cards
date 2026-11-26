# Chatwoot — תיבת פניות לקוחות (קוד פתוח, חינמי)

Chatwoot מאחד במקום אחד את כל ההודעות מלקוחות: וואטסאפ, אינסטגרם, פייסבוק,
מייל, טלגרם וצ'אט באתר. כמה נציגים יכולים לענות, יש תגיות, תשובות מוכנות,
בוט, ודוחות. הגרסה שמותקנת כאן היא הגרסה החינמית בהתקנה עצמית (self-hosted).

## התקנה על שרת (פעם אחת)

צריך שרת לינוקס (Ubuntu) עם לפחות 4GB זיכרון, למשל Hetzner / DigitalOcean.

```bash
git clone https://github.com/yair7883-cyber/ictera-cards.git
cd ictera-cards/chatwoot
./install.sh https://chat.your-domain.com
```

הסקריפט מתקין Docker אם חסר, יוצר קובץ `.env` עם סיסמאות אקראיות,
מכין את מסד הנתונים ומפעיל הכל. אחר כך נכנסים לכתובת ויוצרים חשבון מנהל.

Chatwoot מאזין רק על `127.0.0.1:3000`. כדי לפתוח אותו לאינטרנט עם HTTPS
שמים לפניו Caddy (הכי פשוט):

```bash
sudo apt install -y caddy
echo 'chat.your-domain.com {
  reverse_proxy 127.0.0.1:3000
}' | sudo tee /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

## פקודות שימושיות

| מה | פקודה |
|---|---|
| מצב השירותים | `docker compose ps` |
| לוגים | `docker compose logs -f rails` |
| עצירה | `docker compose down` |
| עדכון גרסה | לשנות את `v4.20.1` ב-`docker-compose.yaml`, ואז `docker compose pull && docker compose run --rm rails bundle exec rails db:chatwoot_prepare && docker compose up -d` |

## קבצים

- `docker-compose.yaml` — מבוסס על הקובץ הרשמי של Chatwoot, עם גרסאות נעולות
- `.env.template` — הגדרות (עברית כברירת מחדל, הרשמה פתוחה כבויה)
- `install.sh` — התקנה בפקודה אחת
- `.env` — נוצר בשרת בלבד, לא נכנס ל-git (מכיל סיסמאות)
