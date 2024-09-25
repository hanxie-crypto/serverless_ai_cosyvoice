import { Client } from "@gradio/client";
import fs from 'fs';
const app = await Client.connect("<endpoint>");

// await app.predict(
// 	"/load_example_2", {
//     example_id: 0,
// });
						
const data = await app.predict(
	"/generate_audio_1", {
    _recorded_audio1: {"path":"/root/tmp/d8bcffa469a71afbe701df1ff62b08a3cdded5a6/13601.wav","url":"<endpoint>/file=/root/tmp/d8bcffa469a71afbe701df1ff62b08a3cdded5a6/13601.wav","orig_name":"13601.wav","size":960044,"mime_type":"audio/wav","meta":{"_type":"gradio.FileData"}},
    _recorded_audio2: null,
    _prompt_input_textbox: "今天的不开心就止于此吧，明天依旧光芒万丈哦~，宝贝",
    _language_radio: "same",
    _synthetic_input_textbox: "我们走的每一步，都是我们策略的一部分；你看到的所有一切，包括我此刻与你交谈，所做的一切，所说的每一句话，都有深远的含义。",
    _seed: 1,
    _audio_input_type_radio: "upload_audio",
});

// data 结构如注释所示
console.log(data);

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
const audioFilename = 'custom.mp3';

// 调用函数下载音频
downloadAudio(audioUrl, audioFilename).then(() => {
    console.log(`Audio file saved as ${audioFilename}`);
}).catch((error) => {
    console.error('Error downloading the audio:', error);
});