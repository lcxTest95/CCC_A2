

<template>
  <div class="about">
    <div id="Map" style="width: 2000px;height:812px;"></div>
  </div>
</template>
<script>
import echarts from "echarts";
export default {
  data() {
    return {};
  },
  mounted() {
    this.draw();
  },
  methods: {
    data_process(LatLon, test_data) {
      let data = [];
      let count_LatLon = 0;
      //遍历地图数据
      for (var key in LatLon["features"]) {
        count_LatLon++;
        let name_value = LatLon["features"][key]["properties"]["SA4_CODE"];
        let name_value1 = LatLon["features"][key]["properties"]["STATE_NAME"];
        LatLon["features"][key]["properties"]['name']=name_value;
        if (test_data[name_value]) {
          let json = {
            name: name_value,
            value: test_data[name_value]["pol"]*1000,
            inc: test_data[name_value]["inc"],
            edu: test_data[name_value]["edu"],
			emo: test_data[name_value]["pol"],
            State_name:LatLon["features"][key]["properties"]["SA4_NAME"]+", "+name_value1,
			sa4:LatLon["features"][key]["properties"]["SA4_NAME"]
          };
          data.push(json);
        }
      }
      let count_data = 0;
      return {LatLon:LatLon,data:data};
    },
    //echarts绘制
    draw() {
      let myChart = echarts.init(document.getElementById("Map"));
      myChart.showLoading();
      //获取数据
      let LatLon = require("../assets/json/SA4_2016_AUST.json");
      let test_data = require("../assets/json/test_data.json");
      //数据处理
      let all_data = this.data_process(LatLon, test_data);
      echarts.registerMap("Australia", all_data['LatLon']);
      let option = {
        backgroundColor: 'rgb(169,216,253)',//背景
        title: {
          text: "Australia",
          left: "right"
        },
        tooltip: {
          position: function (point, params, dom, rect, size) {//文本框位置
            return {right: '20px', top: "20px"};
          },
          left: "left",
          trigger: "item",
          showDelay: 0,
          transitionDuration: 0.2,
          formatter: function(params) {//文本框内容
            // console.log(params);
            var value = (params.value + "").split(".");
            value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, "$1,");
            return "SA4 Code:" + params.data.name + "<br/>" + params.data.State_name + "<br/> Emotion:" + params.data.emo + "<br/> Income:" + params.data.inc + "<br/>Education Index:" +params.data.edu;
          }
        },
        //右下角图例
        visualMap: {
          left: "right",
          min: -1000,
          max: 1000,
          inRange: {
            color: [
              "#313695",
              "#4575b4",
              "#74add1",
              "#abd9e9",
              "#e0f3f8",
              "#ffffbf",
              "#fee090",
              "#fdae61",
              "#f46d43",
              "#d73027",
              "#a50026"
            ]
          },
          text: ["High", "Low"], // 文本，默认为数值文本
          calculable: false
        },
        //左上角的工具栏
        toolbox: {
          show: true,
          //orient: 'vertical',
          left: "left",
          top: "top",
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        series: [
          {
            name: "Australia",
            type: "map",
            roam: true,
            aspectScale:0.9,
            zoom:1.3,
            map: "Australia",
            emphasis: {
              label: {
                show: true,//地图块显示
                formatter:function(params){
                  console.log(params)
                                return params.data.sa4;
                            },
              },
            },
            // 文本位置修正
            textFixed: {
              Alaska: [20, -20]
            },
            data: all_data['data']
          }
        ]
      };
      myChart.hideLoading();//echarts加载状态关闭
      myChart.setOption(option);//绘画echarts
    }
  }
};
</script>
<style scoped>
.about{
  display: flex;
  justify-content: center;
}
</style>
