<template lang="html">
  <div class="main">
    <div class="slider">
      <button type="button" @click="Switch()" id="buttonLeft" style="z-index:1">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-left-short" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5z"/>
        </svg>
      </button>
      <div v-for="item in stas"
      :key="item.id"
      :style="{'background-image': 'url(' + require('@/assets/' + item.photo) + ')', 'display': item.display , 'z-index': 0,}"
      :id="item.id"
      class="slide"
      >
        {{ item.text }}
      </div>
      <button type="button" @click="SwitchTwo()" id="buttonRight" style="z-index:1" ref="bR">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-right-short" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M4 8a.5.5 0 0 1 .5-.5h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5A.5.5 0 0 1 4 8z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{
      count:0,
      stas:[
        {
          id:2,
          display: 'block',
          photo: 'kit.jpeg'
        },
        {
          id:1,
          display: 'block',
          photo: 'kit1.jpeg'
        },
        {
          id:0,
          display: 'block',
          photo: 'kit2.jpeg'
        },
      ]
    }
  },
  mounted(){

  },
  methods:{
    Switch(){
    let self = this;
    let elemOne = document.getElementById(this.count - 1);
    let elemTwo = document.getElementById(this.count);
    if(this.count > 0){
      elemOne.style.marginLeft = "0px"
      this.count -= 1
     }
     else{
       this.count = 2
       for (let i = 0; i < this.count; i++) {
         let element = document.getElementById(i)
         function delay(elem){
           elem.style.marginLeft = '500px';
           function del(){
             elem.style.display = 'block';
           }
           setTimeout(del,500)
         }
         setTimeout(delay(element), 50)
       }
     }
    },
    SwitchTwo(){
    let self = this;
    let elemOne = document.getElementById(this.count - 1);
    let elemTwo = document.getElementById(this.count);
      if(this.count < this.stas.length - 1){
          function animation(elem){
            elem.style.marginLeft = '-500px';
            if(self.count < self.stas.length ){
              setTimeout(function delay(){
                elem.style.display = 'none';
                elem.style.marginLeft = '500px';
                  setTimeout(function del(){
                    elem.style.display = 'block';
                  },50)
              },500)
            }
          }
        animation(elemTwo)
        this.count += 1;
      }
      else{
      for (let i = 1; i < this.stas.length; i++) {
          let elems = document.getElementById(i - 1);
          elems.style.marginLeft = "0px";
        }
        this.count = 0;
      }
    }
  }
}
</script>

<style lang="css" scoped>
.main{
  margin-top: 20px;
  display: flex;
  flex-direction: row;
}
.slider{
  width: 100%;
	height: 300px;
	margin: auto;
	position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  overflow: hidden;
}
.slide{
  width: 100%;
	height: 100%;
	position: absolute;
	top: 0;
	left: 0;
  transition: 0.55s;
  background-size: cover;
}
.sli1{
  background: green;
}
.sli2{
  background: red;
}
.sli3{
  background: blue;
}
button{
  background: none;
  border: none;
  width: 50px;
  height: 50px;
}
svg{
  color: white;
}
@media (max-width: 580px) {
 .slider{
   height: 250px;
 }
}
</style>
