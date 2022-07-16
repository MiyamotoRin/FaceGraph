<template>
  <div>
    <label v-if='!value' class='upload-content-space user-photo default'>
      <input ref='file' class='file-button' type='file' @change='upload' />
      アップロードする
    </label>

    <button type='button' class='delete-button' @click='deleteImage'>
      削除する
    </button>

    <div v-if='value' class='uploaded'>
      <label class='upload-content-space user-photo'>
        <input ref='file' class='file-button' type='file' @change='upload' />
        <img class='user-photo-image' :src='value' />
      </label>
    </div>

    <ul v-if='fileErrorMessages.length > 0' class='error-messages'>
      <li v-for='(message, index) in fileErrorMessages' :key='index'>
        {{ message }}
      </li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'Upload',
  props: {
    value: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      file: null,
      fileErrorMessages: [],
      message: '', // 入力データを格納する変数。
      result: '', // 演算結果を格納する変数。
      state: 'wait', // 現在の状況を格納する変数。
      image: '',
      resultImages: []
    }
  },
  methods: {
    // 画像のBase64のデータをバックエンドに送り、バックエンドから演算結果を受け取り、その結果を表示するメソッド
    getImage (file) {
      this.state = 'getting data'
      const data = new FormData()
      data.append('image', file)
      const config = {headers: {"content-type": "multipart/form-data",}}
      console.log(data.getAll('image'))
      this.$axios.post('http://localhost:3000/api', data, config)
        .then(function (response) {
          this.result = response.data.resultImages
          this.$emit('input', String(this.result[0]));
          // this.state = 'done'
        }.bind(this)) // Promise処理を行う場合は.bind(this)が必要
        .catch(function (error) { // バックエンドからエラーが返却された場合に行う処理について
          // this.state = 'ERROR'
          console.log(error)
        })
        .finally(function () {
        })
    },
    async upload(event) {
      const files = event.target.files || event.dataTransfer.files;
      const file = files[0];

      if (this.checkFile(file)) {
        const picture = await this.getBase64(file);
        this.getImage(file)
      }
    },
    deleteImage() {
      this.$emit('input', null);
      this.$refs.file = null;
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      })
    },
    checkFile(file) {
      let result = true;
      this.fileErrorMessages = []
      const SIZE_LIMIT = 5000000; // 5MB
      // キャンセルしたら処理中断
      if (!file) {
        result = false;
      }
      // jpeg か png 関連ファイル以外は受付けない
      if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
        this.fileErrorMessages.push('アップロードできるのは jpeg画像ファイル か png画像ファイルのみです。')
        result = false;
      }
      // 上限サイズより大きければ受付けない
      if (file.size > SIZE_LIMIT) {
        this.fileErrorMessages.push('アップロードできるファイルサイズは5MBまでです。')
        result = false;
      }
      return result;
    },
  },
};
</script>

<style scoped>
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
  max-width: 85px;
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