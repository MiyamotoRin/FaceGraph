<template>
  <div>
    <div v-if="!value" class="mid-block">
      <div class="left-block">
        <p>Let's play your face!</p>
        <div class="left-desc">
          ア<span>ッ</span>プロードされた顔画像を歪ませる<br/>ことで、様々なデータを表情で<br>視ることができますよ。
          <br/><br/>csvファイルは<br/>なくても<br/>動くよ<br/>！
        </div>
        <div class="left-buttons">
          <label v-if="!value" class="upload-content-space user-photo default">
            <input
              ref="file"
              class="file-button"
              type="file"
              @change="imgUpload"
            />
            画像を選択
          </label>

          <label
            v-if="!csvFile"
            class="upload-content-space user-photo default"
          >
            <input
              ref="file"
              class="file-button"
              type="file"
              @change="csvUpload"
            />
            csvファイルを選択
          </label>

          <label v-if="csvFile">{{ csvFile }}</label>

          <label class="upload-content-space user-photo default">
            <input class="file-button" @click="postData" />
            作成
          </label>
        </div>
      </div>
      <div class="right-block">
        <div class="sample-photo">
          <img src="../assets/sampleDistort.png" />
        </div>
      </div>
    </div>

    <div v-if="value" class="uploaded">
      <div class="buttons">
        <button type="button" class="button-space delete-button" @click="deleteImg">
          画像を削除
        </button>

        <label v-if="!csvFile" class="button-space user-photo default">
          <input
            ref="file"
            class="file-button"
            type="file"
            @change="csvUpload"
          />
          csvファイルを選択
        </label>
        <button type="button" class="button-space delete-button" @click="deleteCsv">
          csvファイルを削除
        </button>

        <label class="button-space user-photo default">
          <input class="file-button" @click="postData" />
          作成
        </label>
      </div>
      <div class="mae-img">
        <label class="upload-content-space user-photo">
          <input
            ref="file"
            class="file-button"
            type="file"
            @change="imgUpload"
          />
          <img class="user-photo-image" :src="value" />
        </label>
      </div>
      <div v-if="resultImages.length" class="procImages">
        <span v-for="(resultImage, index) in resultImages" :key="index">
          <img :src="resultImage" />
        </span>
      </div>
    </div>

    <ul v-if="fileErrorMessages.length > 0" class="error-messages">
      <li v-for="(message, index) in fileErrorMessages" :key="index">
        {{ message }}
      </li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: "Upload",
  props: {
    value: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      imgFile: null,
      csvFile: null,
      fileErrorMessages: [],
      message: "", // 入力データを格納する変数。
      result: null, // 演算結果を格納する変数。
      state: "wait", // 現在の状況を格納する変数。
      image: "",
      resultImages: [],
    };
  },
  methods: {
    // 画像のBase64のデータをバックエンドに送り、バックエンドから演算結果を受け取り、その結果を表示するメソッド
    postData() {
      const data = new FormData();
      data.append("files", this.imgFile, "img");
      if (this.csvFile !== null) {
        data.append("files", this.csvFile, "csv");
      } else {
        // csvが読み込まれなかった場合にはデフォルトのものを読み込む
        let blob = new Blob(["no file selected"], { type: "text/plain" });
        data.append("files", blob, "NoFile");
        console.log("デフォルト");
      }
      const config = { headers: { "content-type": "multipart/form-data" } };
      this.$axios
        .post("http://localhost:3000/api", data, config)
        .then(
          function (res) {
            this.resultImages = res.data.resultImages;
            console.log("ok");
            console.log(res.data.resultImages);
          }.bind(this)
        ) // Promise処理を行う場合は.bind(this)が必要
        .catch(function (error) {
          // バックエンドからエラーが返却された場合に行う処理について
          console.log(error);
        })
        .finally(function () {});
    },
    async imgUpload(event) {
      const files = event.target.files || event.dataTransfer.files;
      const file = files[0];

      if (this.imgCheckFile(file)) {
        this.imgFile = file;
        const picture = await this.getBase64(file);
        this.$emit("input", picture);
      }
    },
    deleteImg() {
      this.$emit("input", null);
      this.$refs.imgFile = null;
    },
    deleteCsv() {
      this.$refs.csvFile = null;
    },
    async csvUpload(event) {
      const files = event.target.files || event.dataTransfer.files;
      const file = files[0];

      if (this.csvCheckFile(file)) {
        this.csvFile = file;
      }
    },
    imgCheckFile(file) {
      let result = true;
      this.fileErrorMessages = [];
      const SIZE_LIMIT = 5000000; // 5MB
      // キャンセルしたら処理中断
      if (!file) {
        result = false;
      }
      // jpeg か png 関連ファイル以外は受付けない
      if (file.type !== "image/jpeg" && file.type !== "image/png") {
        this.fileErrorMessages.push(
          "アップロードできるのは jpeg画像ファイル か png画像ファイルのみです。"
        );
        result = false;
      }
      // 上限サイズより大きければ受付けない
      if (file.size > SIZE_LIMIT) {
        this.fileErrorMessages.push(
          "アップロードできるファイルサイズは5MBまでです。"
        );
        result = false;
      }
      return result;
    },
    csvCheckFile(file) {
      let result = true;
      this.fileErrorMessages = [];
      const SIZE_LIMIT = 5000000; // 5MB
      // キャンセルしたら処理中断
      if (!file) {
        result = false;
      }
      // csv 関連ファイル以外は受付けない
      if (file.type !== "text/csv") {
        this.fileErrorMessages.push(
          "アップロードできるのは csv画像ファイルのみです。"
        );
        result = false;
      }
      // 上限サイズより大きければ受付けない
      if (file.size > SIZE_LIMIT) {
        this.fileErrorMessages.push(
          "アップロードできるファイルサイズは5MBまでです。"
        );
        result = false;
      }
      return result;
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },
  },
};
</script>

<style scoped>
.mid-block {
  display: flex;
}
.left-block {
  width: 60%;
  display: flex;
  flex-direction: column;
  justify-content:space-between;
  padding-bottom:10px;
  align-items: center;
}
.left-desc{
  text-align: center;
  padding:0% 10% 10% 15%;
  width:100%;
  font-size:1.2em;
  color:#2d4059;
  font-weight: 550;
  line-height: 110%;
}
.left-desc > span{
  font-size:0.85em;
}
.left-buttons{
  display: flex;
  margin-bottom:0%;
}

p {
  font-size: 50px;
  font-family: serif;
  color:#2d4059;
  font-weight: 600;
}
.right-block {
  width: 40%;
  display:flex;
  justify-content: center;
}
.sample-photo > img {
  margin:20px 0px;
}
.procImages {
  display: flex;
}
.procImages > img {
  width: 75px;
}
.buttons {
  display: flex;
  width: 100%;
}

.user-photo.default {
  cursor: pointer;
  outline: none;
  align-items: center;
  background-color: #2d4059;
  border: 3px solid #bdbdbd;
  border-radius: 2px;
  box-sizing: border-box;
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0.3px;
  color: #ffd460;
  height: 4rem;
  padding: 0 1.6rem;
  max-width: 400px;
  margin: 0px 10px;
}
.button-space{
  margin:0px 20px;
}

.user-photo.default:hover {
  background-color: #bdbdbd;
  border: 3px solid #2d4059;
  color: #fd8700;
}

.user-photo.default:active {
  background-color: #0051b0;
}

.user-photo-image {
  max-width: 50%;
  display: block;
}

.user-photo-image:hover {
  opacity: 0.8;
}

.file-button {
  display: none;
}

.uploaded {
  align-items: center;
}

.delete-button {
  cursor: pointer;
  outline: none;
  align-items: center;
  background-color: #2d4059;
  border: 3px solid #bdbdbd;
  border-radius: 2px;
  box-sizing: border-box;
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0.3px;
  color: #ea5455;
  height: 4rem;
  padding: 0 1.6rem;
  max-width: 400px;
  margin: 0px 10px;
}

.delete-button:hover {
  background-color: #bdbdbd;
  border: 3px solid #2d4059;
  color: #e62a2a;
}

.error-messages {
  color: #cf0000;
  list-style: none;
  margin: 0.4rem 0 0 0;
  padding: 0 0.2rem;
  font-size: 1.6rem;
}
</style>