<template>
  <div>
    <div
      v-for="(item, index) in dartScores"
      v-bind:key="index"
      :style="{ padding: '5px', 'background-color': getTurn(index) }" @mouseover="showPencil = true"  @mouseleave="showPencil = false"
    >
      <v-row cols="1" sm="8" class="ma-2">
        <div class="justify-center">
          <img
            src="../assets/dart.png"
            width="30"
            height="30"
            style="padding: 2px"
          />
        </div>
        <div
          v-if="isNumeric(item.score)"
          style="padding-left: 10px; margin-top: 2px; font-size: 20px"
        >
          <v-icon>mdi-equal</v-icon>{{ item.score }}
        </div>
        <div v-else style="padding-left: 8px">
          <v-icon>mdi-equal</v-icon> {{ item.score }} <!-- change later-->
        </div>
        <!--div @mouseover="showPencil = true"  @mouseleave="showPencil = false"-->
        <img v-show="showPencil" @click="showInput=true" @dblclick="showInput=false"
            src="../assets/pencil.png"
            width="30"
            height="30"
            style="padding: 2px;margin-left:38px;"
          />
      </v-row>
      <v-text-field v-show="showInput"
                    class="mt-n6"
                    v-model="corrected"
                    placeholder="enter text"
                    v-on:keyup.enter="onEnter(index)"
                  ></v-text-field>
                  
      <v-divider></v-divider>
    </div>
  </div>
</template>

<script>
export default {
  name: "DartScorer",
  props: ["dartScores"],
  data: function () {
    return {
      showPencil:false,
      showInput:false,
      corrected:0,
    };
  },
  created() {
    this.$root.$refs.DartScorer = this;
  },
  methods: {
    getTurn(index) {
      if (this.dartScores[index].score == 0) {
        return "lightgreen";
      } else {
        return "tranparent";
      }
    },
    onEnter: function(index) {
      this.showInput=false;
      this.dartScores[index].score=this.corrected
    },
    isNumeric(value) {
      return Number.isInteger(value)
    },
    getDebug(){
      for(let i = 0;i<this.dartScores.length;i++) {
        console.log(this.dartScores[i].score)
      }
    },
    getScore_all_tries_together(){
      let finaladditonScore = 0;
      for(let i= 0;i<this.dartScores.length;i++) {
        finaladditonScore+=this.dartScores[i].score
      }
      return finaladditonScore
    },
  },
};
</script>

<style>
#shootout {
  display: relative;
}
.head {
  display: grid;
  grid-template-columns: 2fr 1fr;
  place-items: center;
  /*border: 5px solid black;*/
}

.players {
  display: flex;
  color: white;
}
.record {
  background-color: #333;
}
h1 {
  background-color: lightblue;
  text-align: center;
}
h2 {
  padding: 10px 0px 0px 0px;
}
h3 {
  color: lightblue;
}
.record > div {
  color: white;
  font-weight: bold;
  font-size: 1rem;
  border: 2px solid white;
  padding: 10px;
  min-width: 150px;
  min-height: 45px;
}
.players > div {
  padding: 10px;
  border-left: 4px solid black;
  border-bottom: 4px solid black;
}
.players > div:last-child {
  border-right: 4px solid black;
}
h3 {
  margin: 0 0 5px 0;
}
.score {
  background-color: #333;
  border-radius: 5px;
  text-align: center;
  color: #fff;
}

.nextPlayer {
  padding-top: 20px;
  text-align: center;
}

.scorePoint {
  font-size: 300px;
  text-align: center;
  color: lightgreen;
}
.player {
  background-color: #333;
  flex-grow: 1;
  padding: 1px 0px 0px 14px;
  color: #fff;
  border-radius: 5px;
}
</style>

