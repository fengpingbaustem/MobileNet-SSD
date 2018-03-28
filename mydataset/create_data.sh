cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
redo=1
data_root_dir=$cur_dir
dataset_name=myface
#VOC格式数据存放的文件夹data_root_dir="$cur_dir/mydataset"
#训练集还是测试集，只是标识一下，就是放在一个文件夹里，放test或者train都是可以的，这样只是为了方便切换相同数据库的不同文件夹type=test
#数据库名称，只是标记VOC数据在mydataset下面的哪个文件夹里面，结果又放在哪个文件夹里面。dataset_name="ICDAR2013"
mapfile="$cur_dir/result/$dataset_name/labelmap.prototxt"
anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0
 
extra_cmd="--encode-type=jpg --encoded"
if [ $redo ]
then
  extra_cmd="$extra_cmd --redo"
fi
for subset in test train
do
  #最后一个参数是快捷方式所在的位置，不用建这个文件夹，但是为了代码改的少参数还是要有，我们在下面的create_annoset.py注释掉了生成快捷方式那句。  
  #echo --anno-type=$anno_type --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim --resize-width=$width --resize-height=$height --check-label $extra_cmd $data_root_dir result/$dataset_name/$subset.txt result/$dataset_name/$dataset_name"_"$subset"_"$db result/$dataset_name
  python create_annoset.py --anno-type=$anno_type --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim --resize-width=$width --resize-height=$height --check-label $extra_cmd $data_root_dir result/$dataset_name/$subset.txt result/$dataset_name/$dataset_name"_"$subset"_"$db result/$dataset_name
done