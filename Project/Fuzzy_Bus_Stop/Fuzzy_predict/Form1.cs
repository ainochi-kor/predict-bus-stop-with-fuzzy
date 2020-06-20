using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Collections;

namespace Fuzzy_predict
{
    public partial class Form1 : Form
    {
        //Fuzzy_Bus_Stop\Fuzzy_predict\bin\Debug에서 기준.
        string file_path;
        string file_save = "Sort_Bus_Data_txt\\";
        string file_name = null;

        //버스 지연시간을 최대 30분으로 잡는다.
        int[] delay_times = new int[30]; 
        int count = 0, csv_index_4 = 0, csv_index_4_temp = 0;

        //csv파일의 행을 담당.
        ArrayList row = new ArrayList(); 
        ArrayList new_arrBusStop = new ArrayList();
        ArrayList arr_predict = new ArrayList();
        ArrayList arr_fuzzyTimes = new ArrayList();

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        public void FileSave(string path, string txt)
        {
            //파일 스트림을 이용하여, 쓰기
            FileStream fileStream = new FileStream(path, FileMode.Append);
            StreamWriter s_Writer = new StreamWriter(fileStream);

            //txt 파일을 쓰기
            s_Writer.WriteLine(txt);

            s_Writer.Close();
            fileStream.Close();
        }

        public void FileRead(string path)
        {
            //파일을 읽고 읽는다.
            FileStream fileStream = new FileStream(path, FileMode.Open);
            StreamReader s_read = new StreamReader(fileStream);

            string line;
            int line_num = 0;

            // line에 한줄을 읽고 값이 있으면 실행
            while ((line = s_read.ReadLine()) != null)
            {
                // count가 1보다 크면서 짝수이면 해당 CSV파일의 값을 가져오기 위함.
                if (line_num > 1 && line_num % 2 == 0)
                {
                    //들어온 row의 값의 columns를 배열로 저장
                    string[] columns = null;
                    //csv파일 특성 상 쉼표를 이용하여 columns을 구분
                    columns = line.Split(','); 
                    //columns에 있는 배열의 값을 하나씩 row에 추가함.
                    foreach (string column in columns)
                    {
                        //row배열에 column을 추가함.
                        row.Add(column);
                    }
                }
                //행의 숫자를 증가시킴.
                line_num++;
            }

            s_read.Close();
            fileStream.Close();
        }

        public void FileReadTxt(string path)
        {
            FileStream fileStream = new FileStream(path, FileMode.Open);
            StreamReader s_read = new StreamReader(fileStream);

            string line;
            int delay_min = 0;

            while ((line = s_read.ReadLine()) != null)
            {
                //지연배열[ 배열의 순서 ] == 지연 분
                delay_times[delay_min] = Convert.ToInt32(line);
                delay_min++;
            }

            s_read.Close();
            fileStream.Close();
        }

        public void MakeFolder()
        {
            //새 디렉토리를 만들어서 사용한 값을 저장.
            file_save = file_save + DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss") + file_name;
            DirectoryInfo make_folder = new DirectoryInfo(file_save);
            make_folder.Create();
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //파일 패스를 초기화.
            file_path = "Sort_Bus_Data\\";
            //시간이 오후 5시가 넘어가는가?
            if (Convert.ToInt32(textBox4.Text) >= 17)
            {
                //PM파일을 읽어온다.
                file_path += "Sort_Bus_Data_by" + textBox2.Text + "_PM.csv";

                //csv 시작 시를 변수에 저장
                csv_index_4 = 17;
                csv_index_4_temp = 17;
            }
            else
            {
                file_path += "Sort_Bus_Data_by" + textBox2.Text + "_AM.csv";

                //csv 시작 시를 변수에 저장
                csv_index_4 = 7;
                csv_index_4_temp = 7;
            }

            //파일 이름을 버스번호로 저장
            file_name = file_path.Split('\\')[1];
            
            FileRead(file_path);

            function_new_arrBusStop(textBox3.Text);

            function_arr_predict();

            function_arr_fuzzyTimes();
            
            Fuzzy_Predict();
        }

        public void function_new_arrBusStop(string busStop_num)
        {
            int column_num = 0;
            while (true)
            {
                if (column_num >= row.Count)
                {
                    break;
                }
                else
                {
                    if (Convert.ToInt32(row[column_num]) == Convert.ToInt32(busStop_num))
                    {
                        new_arrBusStop.Add(row[column_num]);     // 정류장 번호
                        new_arrBusStop.Add(row[column_num + 3]); // 날짜
                        new_arrBusStop.Add(row[column_num + 4]); // 시
                        new_arrBusStop.Add(row[column_num + 5]); // 분
                        new_arrBusStop.Add(row[column_num + 7]); // 도착 예상 시
                        new_arrBusStop.Add(row[column_num + 8]); // 도착 예상 분
                    }
                }
                column_num += 9; // 다음 행으로 이동.
            }
            row.Clear();
        }

        public void function_arr_predict()
        {
            double before_now_time = 0.0, before_stop_time = 0.0, now_time = 0.0, delay_time_1 = 0.0, delay_time_2 = 0.0, delay_time_3 = 0.0, predict_time = 0.0;
            Boolean predict = false;

            int standard_column = 6;

            while (true)
            {
                //bus_times_extract 배열의 크기가 더 크면 예측 시간에 저장
                if ((standard_column + 1) > new_arrBusStop.Count)
                {
                    arr_predict.Add(predict_time);
                    break;
                }
                else
                {
                    //같은 정류장끼리 계산하기 위한 if문
                    if (DateTime.Parse(new_arrBusStop[standard_column + 1].ToString()) != DateTime.Parse(new_arrBusStop[standard_column - 5].ToString()))
                    {
                        standard_column += 6;
                        continue;
                    }
                    //이전 시와 분을 초로 변환하고 시간을 저장. 
                    before_now_time = (Convert.ToDouble(new_arrBusStop[standard_column - 4])) * 3600 + (Convert.ToDouble(new_arrBusStop[standard_column - 3]) * 60);
                    //이전 도착 예상 시와 분을 초로 변환하고 시간을 저장.
                    before_stop_time = (Convert.ToDouble(new_arrBusStop[standard_column - 2])) * 3600 + (Convert.ToDouble(new_arrBusStop[standard_column - 1]) * 60);
                    //다음 해당 시간의 시와 분을 초로 변환하고 시간을 저장
                    now_time = (Convert.ToDouble(new_arrBusStop[standard_column + 2])) * 3600 + (Convert.ToDouble(new_arrBusStop[standard_column + 3]) * 60);

                    /*
                     * 이전 도착 시간과 현재시간이 같거나, 
                     * 이전 도착 시간과 이전 도착시간이 같거나, 
                     * 이전 도착 시간 - 현재시간과의 차가 1분 이하인 경우
                     */
                    if (before_stop_time == now_time || before_now_time == before_stop_time || before_stop_time - now_time <= 1)
                    {
                        //
                        if (predict)
                        {

                            arr_predict.Add(predict_time);
                            predict_time = 0.0;
                        }

                        predict = false;
                    }
                    else
                    {
                        if (predict_time <= 0.0)
                        {
                            arr_predict.Add(new_arrBusStop[standard_column - 5]); //날짜
                            arr_predict.Add(new_arrBusStop[standard_column - 4]); //시
                            arr_predict.Add(new_arrBusStop[standard_column - 3]); //분
                        }

                        delay_time_1 = Math.Abs((before_stop_time - now_time) / 60); //이전 도착 시간 - 해당 시간 
                        delay_time_2 = Math.Abs((now_time - before_now_time) / 60); //해당 시간 - 이전 현재 시간
                        delay_time_3 = Math.Abs((before_stop_time - before_now_time) / 60); //이전 도착 시간 - 이전 현재 시간

                        if ((delay_time_3 == delay_time_1 + delay_time_2) && predict_time != 0.0)
                        {
                            //지연이 안되었기에 계산 하지 않음.
                        }
                        else
                        {
                            //지연된 시간을 predict_time변수에 저장.
                            predict_time += delay_time_3;
                        }
                        //지연 시간을 저장했으니, true로 변환
                        predict = true;
                    }
                }
                //기준 칼럼을 6 증가 시킨다. 왜냐하면 csv파일 6개씩 들고왔으니까.
                standard_column += 6;
            }
            //새롭게 가져온 배열의 요소를 제거.
            new_arrBusStop.Clear();
            MakeFolder();

            int max = 0;
            do {
                for (count = 0; count < arr_predict.Count; count += 4)
                {
                    //예측 배열의 시간과 csv_index_4(csv파일의 현재 시)가 같은가?
                    if (Convert.ToInt32(arr_predict[count + 1]) == csv_index_4)
                    {
                        //지연된 분의 배열에 값을 +1 시킨다.
                        delay_times[Convert.ToInt32(arr_predict[count + 3]) - 1] = delay_times[Convert.ToInt32(arr_predict[count + 3]) - 1] + 1;

                        //텍스트 파일에 들어가는 분의 갯수를 계산
                        if (max < Convert.ToInt32(arr_predict[count + 3]))
                        {
                            max = Convert.ToInt32(arr_predict[count + 3]);
                        }
                    }
                }
                //파일 주소와 내용을 매개변수로 넘겨서 파일을 저장
                for (int i = 0; i < max; i++)
                    FileSave(file_save + "\\" + csv_index_4 + "Hour.txt", delay_times[i].ToString());
                

                //초기화
                delay_times = new int[30];
                max = 0;
                //csv파일의 시간을 증가
                csv_index_4++;
                //csv파일이 보유한 시간들.
            } while (csv_index_4 < 24 && csv_index_4 > 7 && csv_index_4 != 17);
        }

        public void function_arr_fuzzyTimes()
        {
            int traffic_count = 0, delay_time = 0;
            //csv의 csv_index_4를 csv_index_4_temp에 저장
            csv_index_4 = csv_index_4_temp;

            count = 0;

            do
            {
                //시간 비교
                if (Convert.ToInt32(arr_predict[count + 1]) == csv_index_4)
                {
                    traffic_count++;
                    //다음 날짜
                    delay_time += Convert.ToInt32(arr_predict[count + 3]);
                    
                    if (((count + 5) < arr_predict.Count) && (Convert.ToInt32(arr_predict[count + 5]) != csv_index_4))
                    {
                        delay_time = delay_time / traffic_count;

                        arr_fuzzyTimes.Add(csv_index_4);
                        arr_fuzzyTimes.Add(traffic_count);
                        arr_fuzzyTimes.Add(delay_time);

                        csv_index_4++;
                        traffic_count = 0;
                        delay_time = 0;

                        if (DateTime.Parse(arr_predict[count].ToString()) != DateTime.Parse(arr_predict[count + 4].ToString()))
                        {
                            csv_index_4 = csv_index_4_temp;
                        }
                    }
                    count += 4;
                }
            } while ((count + 1) < arr_predict.Count);

            arr_predict.Clear();
        }

        

        public double membership_function_time(int count, int bus_hour)
        {
            double bus_delay_time = 0.0;
            double fuzzy_min = 0.0, fuzzy_mid = 0.0, fuzzy_max = 0.0;
            double L_sum = 0.0, T_sum = 0.0, R_sum = 0.0;
            double L_count = 0.0, T_count = 0.0, R_count = 0.0;
            double L_result = 0.0, T_result = 0.0, R_result = 0.0;
            double result = 0.0;

            //min을 가져옴.
            bus_delay_time = Double.Parse(arr_fuzzyTimes[count + 2].ToString());
            //삼각함수에서 가져온 min이 어디에 소속되어 있는지 확인
            fuzzy_min = L_square_membership_time(bus_delay_time);
            fuzzy_mid = triangle_membership_time(bus_delay_time); 
            fuzzy_max = R_square_membership_time(bus_delay_time);
            //파일에 저장
            FileReadTxt(file_save + "\\" + bus_hour + "Hour.txt");

            count = 0;

            foreach (int num in delay_times)
            {
                if (count < 5)
                {
                    // 5분 이내의 값들을 모두 더함
                    L_sum += num * (count + 1);
                    // 5분 이내의 값들의 갯수를 더함.
                    L_count += num;
                }
                if (count >= 5 && count < 15)
                {
                    // 6분 이상 15분이하의 값들을 모두 더함
                    T_sum += num * (count + 1);
                    // 갯수를 모두 더함
                    T_count += num;
                }
                if (count > 15)
                {
                    // 16분 이상의 값을 모두 더함
                    R_sum += num * (count + 1);
                    // 갯수를 모두 더함
                    R_count += num;
                }

                count++;
            }

            //무게 중심법
            L_result = ((L_sum / L_count) * fuzzy_min);
            T_result = ((T_sum / T_count) * fuzzy_mid);
            R_result = ((R_sum / R_count) * fuzzy_max);

            if (double.IsNaN(L_result))
            {
                L_result = 0;
            }
            if (double.IsNaN(T_result))
            {
                T_result = 0;
            }
            if (double.IsNaN(R_result))
            {
                R_result = 0;
            }

            //무게 중심법 결과.
            result = L_result + T_result + R_result;

            return result;
        }

        public double triangle_membership_time(double bus_delay_time)
        {
            double fuzzy_triangle = 0.0;
            double triangle_min = 5.0, triangle_mid = 10.0, triangle_max = 15.0;

            if (bus_delay_time == triangle_mid)
                fuzzy_triangle = 1.0;

            else if (bus_delay_time > triangle_mid)
                fuzzy_triangle = (triangle_max - bus_delay_time) / (triangle_max - triangle_mid);

            else if (bus_delay_time < triangle_mid)
                fuzzy_triangle = (bus_delay_time - triangle_min) / (triangle_mid - triangle_min);

            return Math.Truncate(fuzzy_triangle * 100) / 100;
        }

        public double L_square_membership_time(double bus_delay_time)
        {
            double fuzzy_square = 0.0;
            double square_min = 5.0, square_max = 10.0;

            if (bus_delay_time <= square_min)
                fuzzy_square = 1.0;
        
            else
                fuzzy_square = (square_max - bus_delay_time) / (square_max - square_min);

            if (fuzzy_square < 0.0)
                fuzzy_square = 0.0;

            return Math.Truncate(fuzzy_square * 100) / 100;
        }

        public double R_square_membership_time(double bus_delay_time)
        {
            double fuzzy_square = 0.0;
            double square_min = 10.0, square_max = 15.0;

            if (bus_delay_time >= square_max)
                fuzzy_square = 1.0;
            else
                fuzzy_square = (bus_delay_time - square_min) / (square_max - square_min);

            if (fuzzy_square < 0.0)
                fuzzy_square = 0.0;

            return Math.Truncate(fuzzy_square * 100) / 100;
        }

        public void Fuzzy_Predict()
        {
            csv_index_4 = csv_index_4_temp;

            count = 0;

            double result = 0.0;

            while (count < arr_fuzzyTimes.Count)
            {
                if (Convert.ToInt32(arr_fuzzyTimes[count]) == Convert.ToInt32(textBox4.Text))
                {
                    result = membership_function_time(count, csv_index_4);

                    result = Math.Truncate(result);
                    int hours = Convert.ToInt32(textBox4.Text);
                    int mins = Convert.ToInt32(textBox5.Text);
                    int pred_min = Convert.ToInt32(textBox6.Text);

                    mins = mins + pred_min;
                    if (mins > 59)
                    {
                        mins -= 60;
                        hours += 1;
                    }

                    textBox1.Text = "시간 : " + textBox4.Text + "시 " + textBox5.Text + "분\r\n퍼지 추론을 이용한 지연 시간 : " + result + "\r\n버스 도착 예상 시간은 " + hours + "시 " + (mins + result) + "분 ±2";
                    textBox1.Text += Environment.NewLine;

                    textBox1.SelectionStart = textBox1.Text.Length;
                    textBox1.ScrollToCaret();

                    break;
                }

                count += 3;
            }
        }
    }
}
