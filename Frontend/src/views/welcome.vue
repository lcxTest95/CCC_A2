<template>
  <div id="welcome">
    <div class="logo">
		<img
		src="../assets/images/logo1.png"
		alt
		/>
    </div>
    <div class="title">
		<span class="title_text"><p><font face="Fantasy"></font></p></span>
    </div>
    <div class="button_block">
		<el-button @click="tomap">Click Here to Learn More</el-button>
    </div>
  </div>
</template>
<script>
export default {
    methods:{
        tomap(){
           this.$router.push({ path:'/map'})
        }
    }
};
</script>
<!-- Format of the page -->
<style >
#welcome{
  background: url("../assets/images/background.jpg") no-repeat;
  background-size:100% 100%;
}
.logo {
  width: 100%;
  height: 20vh;
}
.logo img {
  float: left;
  width: 150px;
}
.title {
  width: 100%;
  height: 40vh;
  top: 125px
}
.title_text {
  font-size: 6em;
  font-weight: bold;
  color: #ffffff;

}
.button_block{
    width: 100%;
	height: 40vh;
	top: 100px
}
.el-button{
    font-size: 2em;
    padding: 20px 40px;
    border: 1px solid ;
    border-radius: 5px;
}
</style>