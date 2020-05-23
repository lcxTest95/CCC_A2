<template>
  <div id="report">
    <div class="subject">
      <h1>Data Analysis<br/><br/></h1>
      <img src="../assets/images/pic1.png" alt />
	  <p	
	    align="center"
	  >Figure 1. The Word Cloud of Hashtags<br/></p>
	  <p
        align="left"
      >In this part, we processed 462,738 twitter data, each of them has a value of emotion, used Statistical Areas 4 (SA4) to divide the geographical region of Australia. And then we tried to look at whether exist the relationship with local income levels (inc) and the local popularity of education (edu) during the COVID-19. We used the median income per person and the percentage of the persons aged 15 completed year 9 or equivalent, which we got from Aurin, to present those two values of each SA4 region.</p>
      <p
        align="left"
      ><br/>1. Linear Regression<br/>Firstly, we normalized inc and edu, then analyzed each of them to see if there was a linear relationship between it and emotion. From figure 2, we can clearly see that there is no obvious linear trend between these two values and the local average value of emotion (pol). After that, we built a linear regression model, and the coefficient estimates of inc and edu are 0.009 and 0.012. We calculated the MSE, RMSE and the MAE of this model, the values are 0.001, 0.026, 0.018 respectively. Finally, we plotted the predicted value of the pre-partitioned test data against its true value. Thus, we do find that there is no linear relationship between these two variables and pol.</p>
      <img src="../assets/images/pic2.png" alt />
	  <p	
	    align="center"
	  >Figure 2. The Linear Model<br/></p>
	  <img src="../assets/images/pic3.png" alt />
	  <p	
	    align="center"
	  >Figure 3. The Predicted and Actual Values<br/></p>
      <p
        align="left"
      >2. K-NN<br/>We first processed the data and assigned different labels to each region according to different pol. Then we tested different k values one by one and found that when k=8, the accuracy of the model was the highest. We cross-verified the model when k=8. We established two models, one with distance weight and one without. According to the results, the model with weight performed relative better.</p>
      <img src="../assets/images/pic4.png" alt />
      <p	
        align="center"
      >Figure 4. The Accuracy of K-NN with Different Numbers of Neighbors<br/></p>
	  <p
	    align="left"
	  >3. Conclusion<br/>We used two simple regression and classification algorithms, and none of them proved that high income and good education would bring people a better emotion during the COVID-19.</p>
	  
    </div>
  </div>
</template>
<script>
export default {};
</script>
<!-- Format of the page -->
<style scoped>
#report {
  width: 1200px;
  display: flex;
  flex-direction: column;
  /* justify-content:center; */
  margin: 20px auto;
  background: #f3f2ed;
  padding:30px 50px;
  /* margin: 20px 0px; */
}
.subject {
  margin-top: 15px;
}
.subject p {
  text-indent: 0em; 
  font-size: 1.5em; 
  line-height: 50px; 
}
.subject img {
  width: 600px; 
}
</style>