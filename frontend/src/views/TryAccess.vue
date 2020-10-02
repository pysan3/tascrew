<template>
  <div class="wrapper fadeInDown">
    <div id="formContent">
      <!-- Tabs Titles -->
      <h2>{{ pagename[islogin] }}</h2>

      <div id="fadeInClass">
        <!-- Icon -->
        <div class="fadeIn">
          <img src="@/assets/emoji.png">
        </div>

        <!-- Login Form -->
        <input v-for="[key, value] in Array.from(input_info)" :key="key" :id="key" :type="value.type" :placeholder="value.placeholder" v-model="user_info[key]" v-show="(!islogin || value.showOnLogin) && !value.hidden" :required="value.required === true" class="fadeIn">

        <!-- 郵便番号と住所 -->
        <div id="zipcode_input" class="fadeIn" v-show="!islogin">
          <span>〒</span>
          <input type="tel" class="px-0" style="width:3em;" id="zip0" name="zip1" placeholder="000" maxlength="3" v-model="user_info.zipcode[0]" @input="getCompleteAddress(0)">
          <span>-</span>
          <input type="tel" class="px-0" style="width:4em;" id="zip1" name="zip1" placeholder="0000" maxlength="4" v-model="user_info.zipcode[1]" @input="getCompleteAddress(1)">
          <div class="spinner-border spinner-border-sm" v-show="loadAddress"></div>
        </div>
        <input type="text" id="address_main" class="fadeIn" v-show="!islogin" placeholder="address main" v-model="user_info.address[0]">
        <input type="text" id="address_sub" class="fadeIn" v-show="!islogin" placeholder="address sub" v-model="user_info.address[1]">

        <textarea v-show="!islogin" name="ocupation" class="fadeIn" cols="30" rows="10" v-model="user_info.ocupation" placeholder="後で綺麗に実装(キーワードから選択式にしたほうがいい気がする)"></textarea>

        <input type="submit" class="fadeIn" :value="`${pagename[islogin]}`" @click="tryAccess()">

      </div>
      <!-- Remind Passowrd -->
      <div id="formFooter">
        <a class="underlineHover" @click="$router.push({ name: 'tryaccess', params: { page: pagename[islogin ^ 1] }, query: $route.query })">{{ msg[islogin ^ 1] }}?</a>
      </div>

    </div>
  </div>
</template>

<script>
import Axios from 'axios'
import Mixin from '@/mixin'
export default {
  mixins: [Mixin],
  watch: {
    $route (to, from) { // eslint-disable-line no-unused-vars
      this.page_type()
    }
  },
  data () {
    return {
      islogin: 1,
      loadAddress: false,
      pagename: ['signup', 'login'],
      msg: ['make a new account', 'already have an account'],
      user_info: {
        zipcode: ['', ''],
        address: ['', ''],
        prefcode: 0
      },
      input_info: new Map([
        ['user_name', {
          type: 'email',
          placeholder: 'username',
          required: true,
          showOnLogin: true
        }],
        ['user_password', {
          type: 'password',
          placeholder: 'user password',
          required: true,
          showOnLogin: true
        }],
        ['re_password', {
          type: 'password',
          placeholder: 'retype password',
          required: true,
          checkFunc: e => e === this.user_info.user_password,
          error_msg: 'not matching user_password'
        }],
        ['real_name', {
          type: 'text',
          placeholder: 'real name'
        }],
        ['nick_name', {
          type: 'text',
          placeholder: 'nick name'
        }],
        ['email', {
          type: 'email',
          placeholder: 'e-mail',
          required: true,
          checkFunc: e => e.match(/^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]{1,}\.[A-Za-z0-9]{1,}$/)
        }],
        ['phone_number', {
          type: 'tel',
          placeholder: 'phone number',
          required: true,
          checkFunc: e => e.replace(/[━.*‐.*―.*－.*\-.*ー.*-]/gi, '').match(/^(0[5-9]0[0-9]{8}|0[1-9][1-9][0-9]{7})$/)
        }],
        ['zipcode', {
          required: true,
          hidden: true,
          id_name: 'zipcode_input',
          checkFunc: e => e[0].length === 3 && e[1].length === 4
        }],
        ['address', {
          required: true,
          hidden: true,
          id_name: 'address_main',
          checkFunc: e => e[0].length > 0
        }],
        ['ocupation', {
          hidden: true
        }]
      ])
    }
  },
  methods: {
    getCompleteAddress (place) {
      this.loadAddress = true
      if (this.user_info.zipcode[place].length < 3 + place) return
      if (place === 0) {
        document.getElementById('zip1').focus()
      } else {
        Axios.get(`${window.location.protocol}//madefor.github.io/postal-code-api/api/v1/${this.user_info.zipcode.join('/')}.json`).then(response => {
          this.user_info.prefcode = response.data.data[0].prefcode
          const addr = response.data.data[0][this.$i18n.locale]
          this.user_info.address[0] = addr.prefecture + addr.address1 + addr.address2 + addr.address3
          this.user_info.address[1] = addr.address4
          this.loadAddress = false
          document.getElementById('address_main').focus()
        })
      }
    },
    insertErrorMsg (element, msg) {
      const error = document.createElement('div')
      error.innerHTML = msg
      error.style.color = 'red'
      error.className += 'error_msg'
      element.parentNode.insertBefore(error, element.nextSibling)
    },
    requiredError () {
      // すでに表示中のエラーメッセージを一旦消去する
      Array.from(document.getElementsByClassName('error_msg')).forEach(e => {
        if (e.previousSibling.tagName.toLowerCase() === 'input') {
          e.previousSibling.style.border = '2px solid #f6f6f6'
        }
        e.remove()
      })
      let hasError = false
      for (const [key, value] of this.input_info) {
        if (value.required === true) {
          if (value.checkFunc === undefined) {
            value.checkFunc = e => e.length > 0
          }
          if (this.user_info[key] === undefined || !value.checkFunc(this.user_info[key])) {
            const place = document.getElementById(value.id_name || key)
            place.style.borderColor = 'red'
            this.insertErrorMsg(place, value.error_msg || 'more than 1 letter is required')
            hasError = true
          }
        }
      }
      return hasError
    },
    tryAccess () {
      if (!this.islogin && this.requiredError()) {
        alert('やり直してください')
        return
      }
      // 本名やニックネームが未定の場合はユーザ名を適用
      if (this.user_info.real_name === undefined) this.user_info.real_name = this.user_info.user_name
      if (this.user_info.nick_name === undefined) this.user_info.nick_name = this.user_info.user_name
      Axios.post(process.env.VUE_APP_BASE_URL + `/api/${this.pagename[this.islogin]}`, this.user_info).then(async response => {
        if (response.data.isValid === true) {
          const token = response.data.token
          localStorage.setItem('token', token)
          this.$store.commit('set_token', token)
          this.$store.commit('set_loggedin', true)
          this.$emit('rerender', 'header')
          if (this.$route.query.code && (await this.assign2Company(this.$route.query.code))) {
            this.$router.push({
              path: this.$route.query.nexturl !== undefined ? this.$route.query.nexturl.replace('-', '/') : '/',
              query: Object.fromEntries(Object.entries(this.$route.query).filter(([k]) => k !== 'nexturl')),
              force: true
            })
          } else {
            // TODO: push to the page for registering new companies
            this.$router.push('/')
          }
        } else {
          if (response.data.already_taken === true) {
            this.insertErrorMsg(document.getElementById('user_name'), 'this username is already taken.')
          }
          alert(response.data.msg)
        }
      }).catch(error => {
        if (process.env.BUILD_TYPE === 'local') alert(error)
        alert('通信エラーが発生しました。\nやり直してください')
      })
    },
    page_type () {
      const nextpage = this.$route.params.page
      if (nextpage === 'login') this.islogin = 1
      else if (nextpage === 'signup') this.islogin = 0
      else {
        alert('目的地URLが存在しません。')
        this.$router.push('/')
      }
    }
  },
  mounted () {
    this.page_type()
    this.$nextTick().then(() => {
      Array.from(document.getElementById('fadeInClass').children).filter(e => e.style.display !== 'none').forEach((e, i) => {
        e.setAttribute('style', `
          -webkit-animation-delay: ${0.1 * i + 0.3}s;
          -moz-animation-delay: ${0.1 * i + 0.3}s;
          animation-delay: ${0.1 * i + 0.3}s;
        `.replace(/\s/g, ''))
      })
    })
  }
}
</script>

<style lang="stylus" scoped>
img
  width 20%
</style>

<style scoped>
html {
  background-color: #56baed;
}

body {
  font-family: "Poppins", sans-serif;
  height: 100vh;
}

a {
  color: #92badd;
  display:inline-block;
  text-decoration: none;
  font-weight: 400;
}

h2 {
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  display:inline-block;
  margin: 40px 8px 10px 8px;
  color: #cccccc;
}

/* STRUCTURE */

.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  min-height: 100%;
  padding: 20px;
}

#formContent {
  -webkit-border-radius: 10px 10px 10px 10px;
  border-radius: 10px 10px 10px 10px;
  background: #fff;
  padding: 30px;
  width: 90%;
  max-width: 450px;
  position: relative;
  padding: 0px;
  -webkit-box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
  box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
  text-align: center;
}

#formFooter {
  background-color: #f6f6f6;
  border-top: 1px solid #dce8f1;
  padding: 25px;
  text-align: center;
  -webkit-border-radius: 0 0 10px 10px;
  border-radius: 0 0 10px 10px;
}

/* TABS */

h2.inactive {
  color: #cccccc;
}

h2.active {
  color: #0d0d0d;
  border-bottom: 2px solid #5fbae9;
}

/* FORM TYPOGRAPHY*/

input[type=button], input[type=submit], input[type=reset]  {
  background-color: #56baed;
  border: none;
  color: white;
  padding: 15px 80px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  text-transform: uppercase;
  font-size: 13px;
  -webkit-box-shadow: 0 10px 30px 0 rgba(95,186,233,0.4);
  box-shadow: 0 10px 30px 0 rgba(95,186,233,0.4);
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
  margin: 5px 20px 40px 20px;
  -webkit-transition: all 0.3s ease-in-out;
  -moz-transition: all 0.3s ease-in-out;
  -ms-transition: all 0.3s ease-in-out;
  -o-transition: all 0.3s ease-in-out;
  transition: all 0.3s ease-in-out;
}

input[type=button]:hover, input[type=submit]:hover, input[type=reset]:hover  {
  background-color: #39ace7;
}

input[type=button]:active, input[type=submit]:active, input[type=reset]:active  {
  -moz-transform: scale(0.95);
  -webkit-transform: scale(0.95);
  -o-transform: scale(0.95);
  -ms-transform: scale(0.95);
  transform: scale(0.95);
}

input[type=text], input[type=password], input[type=tel], input[type=email] {
  background-color: #f6f6f6;
  color: #0d0d0d;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 5px;
  width: 85%;
  border: 2px solid #f6f6f6;
  -webkit-transition: all 0.5s ease-in-out;
  -moz-transition: all 0.5s ease-in-out;
  -ms-transition: all 0.5s ease-in-out;
  -o-transition: all 0.5s ease-in-out;
  transition: all 0.5s ease-in-out;
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
}

input[type=text]:focus, input[type=password]:focus, input[type=tel]:focus, input[type=email]:focus {
  background-color: #fff;
  border-bottom: 2px solid #5fbae9;
}

input[type=text]:placeholder, input[type=password]:placeholder, input[type=tel]:placeholder, input[type=email]:placeholder {
  color: #cccccc;
}

/* ANIMATIONS */

/* Simple CSS3 Fade-in-down Animation */
.fadeInDown {
  -webkit-animation-name: fadeInDown;
  animation-name: fadeInDown;
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

@-webkit-keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

/* Simple CSS3 Fade-in Animation */
@-webkit-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@-moz-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }

.fadeIn {
  opacity:0;
  -webkit-animation:fadeIn ease-in 1;
  -moz-animation:fadeIn ease-in 1;
  animation:fadeIn ease-in 1;

  -webkit-animation-fill-mode:forwards;
  -moz-animation-fill-mode:forwards;
  animation-fill-mode:forwards;

  -webkit-animation-duration:1s;
  -moz-animation-duration:1s;
  animation-duration:1s;
}

/* Simple CSS3 Fade-in Animation */
.underlineHover:after {
  display: block;
  left: 0;
  bottom: -10px;
  width: 0;
  height: 2px;
  background-color: #56baed;
  content: "";
  transition: width 0.2s;
}

.underlineHover:hover {
  color: #0d0d0d;
}

.underlineHover:hover:after{
  width: 100%;
}

/* OTHERS */

*:focus {
  outline: none;
}

#icon {
  width:60%;
}

</style>
