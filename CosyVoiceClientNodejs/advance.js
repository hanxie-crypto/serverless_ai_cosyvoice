import { Client } from "@gradio/client";
import fs from 'fs';
// 连接到 Gradio 应用
const app = await Client.connect("<endpoint>");

// 发起预测请求
const data = await app.predict(
	"/generate_audio_2", {
    _sound_radio: "中文男",
    _speech_status_textbox: "Selene 'Moonshade', is a mysterious, elegant dancer with a connection to the night. His movements are both mesmerizing and deadly. ",
    _synthetic_input_textbox: "我们走的每一步，都是我们策略的一部分；你看到的所有一切，包括我此刻与你交谈，所做的一切，所说的每一句话，都有深远的含义。",
    _seed: 2,
});

// data 结构如注释所示

// 下载音频
async function downloadAudio(url, filename) {
    const response = await fetch(url);
    const blob = await response.blob();
    const arrayBuffer = await blob.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // 写入文件
    fs.writeFileSync(filename, buffer);
}

// 转换为本地文件
const audioUrl = data.data[0].url;
const audioFilename = 'advance.mp3';

// 调用函数下载音频
const reset = await downloadAudio(audioUrl, audioFilename)