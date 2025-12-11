import axios from "axios";

export async function askGPT(message) {
  try {
    if (!process.env.OPENAI_API_KEY) {
      console.error("OPENAI_API_KEY tidak ditemukan di environment variables");
      return "Maaf, AI service belum dikonfigurasi. Silakan hubungi administrator.";
    }

    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4o-mini", // model yang ringan & murah
        messages: [{ role: "user", content: message }],
        temperature: 0.7,
        max_tokens: 500,
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json",
        },
        timeout: 30000, // 30 second timeout
      }
    );

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error("Error from OpenAI:", error.response?.data || error.message);
    
    if (error.response?.status === 401) {
      return "Maaf, API key OpenAI tidak valid. Silakan periksa konfigurasi backend.";
    } else if (error.response?.status === 429) {
      return "Maaf, quota OpenAI telah habis. Silakan coba lagi nanti.";
    } else if (error.code === 'ECONNREFUSED' || error.message.includes('timeout')) {
      return "Maaf, tidak dapat terhubung ke OpenAI API. Pastikan koneksi internet stabil.";
    }
    
    return "Maaf, terjadi error saat menghubungi AI. Silakan coba lagi.";
  }
}