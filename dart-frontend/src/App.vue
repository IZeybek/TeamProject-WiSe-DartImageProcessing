<template>
  <div id="app">
    <div v-if="game == 0" class="menu">
      <h2>Select game mode</h2>
      <div class="gamemode score1" @click="game = 1; score = 301">301</div>
      <div class="gamemode score2" @click="game = 1; score = 501">501</div>
    </div>
    <div v-else-if="players.length == 0">
      <h2>Select player count</h2>
      <div class="playercount">
        <div @click="setPlayers(1)">1</div>
        <div @click="setPlayers(2)">2</div>
      </div>
    </div>
    <div v-else-if="!gamestarted">
      <h2>Edit player names</h2>
      <div class="playernames">
        <input v-for="index in players.length" v-model="players[index - 1]" :key="index">
      </div>
      <div class="startgame" @click="gamestarted = true">Start game</div>
    </div>
    <div v-else>
      <playfield v-if="game == 1" v-bind:playernames="players" :initialScore="score" v-on:gameover="reset"/>
    </div>
  </div>
</template>

<script>
import playfield from './Playfield.vue'
import './assets/global.css'

export default {
  name: 'app',
  components: {
    playfield
  },
  data: function() {
    return {
      game: 0,
      players: [],
      gamestarted: false,
      score: 301,
    }
  },
  methods: {
    reset() {
      this.game = 0
      this.players = 0
      this.gamestarted = false
    },
    setPlayers(count) {
      const players = []
      for (let i = 0; i < count; i++) {
        players.push("player " + (i+1))
      }
      this.players = players
    }
  }
}
</script>

<style scoped>
.gamemode, .playercount > div, .startgame {
  color: white;
  font-weight: bold;
  padding: 20px 30px;
  cursor: pointer;
}
.score1 {
  background-color: #E40066
}
.score2 {
  background-color: #03CEA4
}
.playercount > div:nth-child(1) {
  background-color: #FB4D3D
}
.playercount > div:nth-child(2) {
  background-color: #03CEA4
}

.line {
  display: flex;
  font-weight: bold;
  padding: 10px;
}
.line:nth-child(even) {
  background-color: #f0f0f0;
}
.name {
  color: #333;
}
.score {
  color: rgb(45, 121, 45);
  margin-left: auto;
}
.playernames {
  display: flex;
  flex-direction: column;
  padding: 30px;
  gap: 20px;
}
.playernames > input {
  max-width: 300px;
}
.startgame {
  background-color: #345995
}
</style>
