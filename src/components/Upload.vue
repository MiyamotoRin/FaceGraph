<template>
  <div>
    <div v-if="!value" class="mid-block">
      <div class="right-block">
        <p>貴方の顔<br />&nbsp;歪めてみませんか・・・</p>
        <label v-if="!value" class="upload-content-space user-photo default">
          <input
            ref="file"
            class="file-button"
            type="file"
            @change="imgUpload"
          />
          画像を選択する
        </label>

        <label v-if="!csvFile" class="upload-content-space user-photo default">
          <input
            ref="file"
            class="file-button"
            type="file"
            @change="csvUpload"
          />
          csvファイルを選択する
        </label>

        <label v-if="csvFile">{{ csvFile }}</label>

        <label class="upload-content-space user-photo default">
          <input class="file-button" @click="postData" />
          作成する
        </label>
      </div>
      <div class="left-block">
        <div class="sample-photo">
          <img src="../assets/sampleDistort.png" />
        </div>
      </div>
    </div>

    <div v-if="value" class="uploaded">
      <div class="buttons">
        <button type="button" class="delete-button" @click="deleteImg">
          画像を削除する
        </button>

        <label v-if="!csvFile" class="upload-content-space user-photo default">
          <input
            ref="file"
            class="file-button"
            type="file"
            @change="csvUpload"
          />
          csvファイルをアップロードする
        </label>
        <button type="button" class="delete-button" @click="deleteCsv">
          csvファイルを削除する
        </button>

        <label class="upload-content-space user-photo default">
          <input class="file-button" @click="postData" />
          作成する
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
      const config = {headers: {"content-type": "multipart/form-data",}}
      this.$axios.post('http://localhost:3000/api', data, config)
        .then(function (res) {
          this.resultImages = res.data.resultImages
          console.log('ok')
          console.log(res.data.resultImages)
        }.bind(this)) // Promise処理を行う場合は.bind(this)が必要
        .catch(function (error) { // バックエンドからエラーが返却された場合に行う処理について
          console.log(error)
        })
        .finally(function () {
        })
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
.right-block {
  width: 50%;
}

p {
  writing-mode: vertical-rl;
  font-size: 50px;
  margin-left: auto;
  margin-right: auto;
  font-family: serif;
}
.left-block {
  width: 50%;
  height: 100%;
}
.sample-photo > img {
  height: 100%;
  margin-top: auto;
  margin-bottom: auto;
}
.buttons {
  display: flex;
  width: 100%;
}

.user-photo {
  cursor: pointer;
  outline: none;
}

.user-photo.default {
  align-items: center;
  background-color: #0074fb;
  border: 1px solid #0051b0;
  border-radius: 2px;
  box-sizing: border-box;
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0.3px;
  color: #fff;
  height: 4rem;
  padding: 0 1.6rem;
  max-width: 177px;
}

.user-photo.default:hover {
  background-color: #4c9dfc;
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
  display: flex;
}

.delete-button {
  background-color: #fff;
  border: none;
  color: #0074fb;
  margin-left: 2rem;
  padding: 0;
}

.delete-button:hover {
  text-decoration: underline;
}

.error-messages {
  color: #cf0000;
  list-style: none;
  margin: 0.4rem 0 0 0;
  padding: 0 0.2rem;
  font-size: 1.6rem;
}
</style>