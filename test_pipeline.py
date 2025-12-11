from ml.chatbot_pipeline import chatbot_pipeline

# Test data
user_interest_answers = ["Mencoba membuat menu sarapan"]
user_tech_answers_mcq = {
    "Apa yang dimaksud dengan Activity dalam pengembangan aplikasi Android?": "Komponen yang menangani tampilan pengguna",
    "Apa fungsi utama dari file AndroidManifest.xml?": "Mendefinisikan struktur dan metadata aplikasi",
    "Dalam konteks Android, apa yang dimaksud dengan Intent?": "Mekanisme untuk navigasi antar Activity"
}

result = chatbot_pipeline(user_interest_answers, user_tech_answers_mcq, student_id="S001")

print("Recommended Module:")
print(result["recommended_module"])
print("\nAll Modules Filtered:")
for mod in result["modules_filtered"]:
    print(mod["course_name"])
