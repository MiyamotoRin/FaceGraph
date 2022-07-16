<template>
  <div>
    <label v-if="!value" class="upload-content-space user-photo default">
      <input ref="file" class="file-button" type="file" @change="upload" />
      csvファイルをアップロードする
    </label>

    <button type="button" class="delete-button" @click="deleteImage">
      削除する
    </button>

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
  name: "csvUpload",
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
    };
  },
  methods: {
    async upload(event) {
      const files = event.target.files || event.dataTransfer.files;
      const file = files[0];

      if (this.checkFile(file)) {
        this.$emit("input", picture);
      }
    },
    deleteImage() {
      this.$emit("input", null);
      this.$refs.file = null;
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },
    checkFile(file) {
      let result = true;
      this.fileErrorMessages = []
      const SIZE_LIMIT = 5000000; // 5MB
      // キャンセルしたら処理中断
      if (!file) {
        result = false;
      }
      // csv 関連ファイル以外は受付けない
      if (file.type !== "text/csv") {
        this.fileErrorMessages.push('アップロードできるのは csvファイル か png画像ファイルのみです。')
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