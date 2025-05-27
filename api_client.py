# api_client.py
import requests

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None

    def login(self, email, password):
        try:
            response = requests.post(f"{self.base_url}/login", data={
                "username": email,       # ⚠️ username olmalı!
                "password": password     # ⚠️ form-data formatı!
            })

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                return {"success": True, "token": self.token, "user": data.get("user")}
            else:
                return {"success": False, "detail": response.json().get("detail")}
        except Exception as e:
            return {"success": False, "detail": str(e)}

    def logout(self):
        self.token = None
        return {"success": True, "message": "Çıkış başarılı"}
    
    def get_available_quizzes(self):
        try:
            response = requests.get(
                f"{self.base_url}/quiz/quizzes",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            print(response.status_code, response.text)  # Debug için
            if response.status_code == 200:
                return {"success": True, "quizzes": response.json()}
            else:
                return {"success": False, "detail": response.json().get("detail")}
        except Exception as e:
            return {"success": False, "detail": str(e)}
        
        
    def get_quiz(self, quiz_id):
        try:
            response = requests.get(
                f"{self.base_url}/quiz/quiz/{quiz_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                return {"success": True, "quiz": response.json()}
            else:
                return {"success": False, "detail": response.json().get("detail")}
        except Exception as e:
            return {"success": False, "detail": str(e)}

    def submit_quiz(self, payload):
        try:
            response = requests.post(
                f"{self.base_url}/submit-quiz",
                json=payload,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                return {"success": True, **response.json()}
            else:
                return {"success": False, "detail": response.json().get("detail", "Hata")}
        except Exception as e:
            return {"success": False, "detail": str(e)}

    def get_quiz_review(self, result_id):
        try:
            response = requests.get(
                f"{self.base_url}/review-quiz/{result_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                data = response.json()
                # Eğer description alanı varsa ve boş/None ise düzelt
                print("Çözüm verisi:", data)  # DEBUG
                if "quiz_title" not in data:
                    data["quiz_title"] = "Untitled Quiz"
                return {"success": True, "review": data}
            else:
                detail = response.json().get("detail", "Bilinmeyen hata")
                return {"success": False, "detail": detail}
        except Exception as e:
            return {"success": False, "detail": str(e)}



    def get_solved_quizzes(self):
        try:
            response = requests.get(
                f"{self.base_url}/quiz/solved",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            print("✅ Çözülen quizler:", response.status_code, response.text)  # DEBUG
            if response.status_code == 200:
                return {"success": True, "quizzes": response.json()}
            else:
                return {"success": False, "detail": response.json().get("detail")}
        except Exception as e:
            return {"success": False, "detail": str(e)}

    def get_team_summary(self):
        try:
            response = requests.get(f"{self.base_url}/team/summary", headers={"Authorization": f"Bearer {self.token}"})
            if response.status_code == 200:
                return {"success": True, "members": response.json()}
            else:
                return {"success": False, "detail": response.json().get("detail")}
        except Exception as e:
            return {"success": False, "detail": str(e)}
        
        
    def get_user_results(self, user_id):
        try:
            res = requests.get(f"{self.base_url}/team/results/{user_id}", headers={"Authorization": f"Bearer {self.token}"})
            if res.status_code == 200:
                return {"success": True, "quizzes": res.json()}
            else:
                return {"success": False, "detail": res.json().get("detail")}
        except Exception as e:
            return {"success": False, "detail": str(e)}


    def get_user_quiz_stats(self):
        try:
            response = requests.get(
                f"{self.base_url}/me/summary-stats",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                return {"success": True, "stats": response.json()}
            else:
                detail = response.json().get("detail", "Bilinmeyen hata")
                return {"success": False, "detail": detail}
        except Exception as e:
            return {"success": False, "detail": str(e)}
