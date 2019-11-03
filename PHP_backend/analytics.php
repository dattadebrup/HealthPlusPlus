<?php  
  $connect = mysqli_connect("35.186.152.172", "root", "", "sihf");  
 $query="SELECT DOB,count(*) as number FROM user GROUP BY DOB";
 $result5=mysqli_query($connect, $query);
 $query= "SELECT disease, count(*) as number FROM history GROUP BY disease";  
 $result1 = mysqli_query($connect, $query);  
 $result3=mysqli_query($connect,$query);
 $query= "SELECT Occupation, count(*) as number FROM user GROUP BY Occupation "; 
 $result4=mysqli_query($connect,$query);
 $query = "SELECT Gender, count(*) as number FROM user GROUP BY Gender";  
 $result2 = mysqli_query($connect, $query);  
 
 ?>  
 <!DOCTYPE html>  
 <html>  
      <head>  
           <title>ANALYTICS PORTAL</title>  
		   <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>  
           <script type="text/javascript">
           
           google.charts.load('current', {'packages':['corechart']});  
           google.charts.setOnLoadCallback(drawChart1); 
			     google.charts.setOnLoadCallback(drawChart2); 
				 google.charts.setOnLoadCallback(drawChart3);
				 google.charts.setOnLoadCallback(drawChart4);
				 google.charts.setOnLoadCallback(drawChart5);
				 function drawChart4() {
        var data = google.visualization.arrayToDataTable([
          ['Occupation', 'Number', ],
		          <?php  
                          while($row = mysqli_fetch_array($result4))  
                          {  
                               echo "['".$row["Occupation"]."', ".$row["number"].",],";  
                          }  
                          ?>  

        ]);

        var options = {
          title: 'Occupation wise fitness analysis',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    function drawChart3() {
      			var data = google.visualization.arrayToDataTable([
      		 	 ["disease", "Number", { role: "style" } ],
        				<?php  
                          while($row = mysqli_fetch_array($result3))  
                          {  
                               echo "['".$row["disease"]."', ".$row["number"].",'gold'],";  
                          }  
                          ?>  
      				]);

			 var view = new google.visualization.DataView(data);
      				view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);
					    var options = {
        		title: "Health v/s number graph",
        		width: 600,
       		 height: 400,
        	bar: {groupWidth: "95%"},
        	legend: { position: "none" },
      		};
      var chart = new google.visualization.ColumnChart(document.getElementById("columnchart_values2"));
      chart.draw(view, options);
  }
  function drawChart5() {
      			var data = google.visualization.arrayToDataTable([
      		 	 ["DOB", "Number", { role: "style" } ],
        				<?php  
                          while($row = mysqli_fetch_array($result5))  
                          {  
                               echo "['".$row["DOB"]."', ".$row["number"].",'green'],";  
                          }  
                          ?>  
      				]);

			 var view = new google.visualization.DataView(data);
      				view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);
					    var options = {
        		title: "Health v/s number graph",
        		width: 600,
       		 height: 400,
        	bar: {groupWidth: "95%"},
        	legend: { position: "none" },
      		};
			var chart = new google.visualization.ColumnChart(document.getElementById("columnchart_values1"));
      chart.draw(view, options);
	  }
    			function drawChart1()  
               {  
                    var data = google.visualization.arrayToDataTable([  
                              ['Gender', 'Number'],  
                              <?php  
                              while($row = mysqli_fetch_array($result2))  
                              {  
                                   echo "['".$row["Gender"]."', ".$row["number"]."],";  
                              }  
                              ?>  
                         ]);  
                    var options = {  
                          title: 'Percentage of gender affected by disease',  
                          //is3D:true,  
                          pieHole: 0.4  
                         };  
                    var chart = new google.visualization.PieChart(document.getElementById('piechart1'));  
                    chart.draw(data, options);  
               }  
           function drawChart2()  
               {  
                    var data = google.visualization.arrayToDataTable([  
                              ['disease', 'Number'],  
                              <?php  
                              while($row1 = mysqli_fetch_array($result1))  
                              {  
                                   echo "['".$row1["disease"]."', ".$row1["number"]."],";  
                              }  
                              ?>  
                         ]);  
                    var options = {  
                          title: 'Percentage of people affected by disease',  
                          //is3D:true,  
                          pieHole: 0.4  
                         };  
                    var chart = new google.visualization.PieChart(document.getElementById('piechart2'));  
                    chart.draw(data, options);  
               }  
           </script>
		   <style>
		   .grid-parent {
		   display:grid;
		   grid-column-gap=1em;
		   grid-row-gap:1em;
		   grid-template-columns: 0.3fr 0.3fr;
		   margin:10px;
		   margin-right:0px;
		   margin-left:12.5%;
		   
		   }
		   h3 {
		   margin-left:12.5%;
			color:#000000;
			font-family: 'Karla';
			font-size: 2em;
		   }
		   .main-heading{color:#000000 ;font-family: 'Karla' ;font-size: 4em;margin-left: 20%;}
		   
		   </style> 
			
      </head>  
      <body>  
           <br /><br />
		   <!--<div class="image">
  				<div><img src="sandcastles.jpg" class="image"></div> 
			</div>-->
      <div class = "main-heading"><b>ONE-STOP ANALYTICS PORTAL</b> </div>
		   <div class="grid-parent" >
           <div class="child" >  
                <h3 >Percentage of male and female population suffering from diseases</h3>  
                <br />  
                <div id="piechart1" style="width: 700px; height: 500px;"></div>  
           </div>  
           <div class="child" >  
                <h3 >Disease distribution among population</h3>  
                <br />  
                <div id="piechart2" style="width: 700px; height: 500px;"></div>  
           </div> 
		   <div class="child" >  
                <h3 >Disease distribution among various age groups</h3>  
                <br />  
                <div id="columnchart_values1" style="width: 700px; height: 500px;"></div>  
           </div>  
		   <div class="child" >  
                <h3>Occupation versus fitness analysis</h3>  
                <br />  
                <div id="curve_chart" style="width: 700px; height: 500px;"></div>  
           </div> 
		   <div class="child" >  
                <h3>Prominence of various diseases</h3>  
                <br />  
                <div id="columnchart_values2" style="width: 700px; height: 500px;"></div>  
           </div>   
          </div>
      </body>  
 </html>  