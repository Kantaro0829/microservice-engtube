FROM python:3.6

# ソースを置くディレクトリを変数として格納                                                  
ARG project_dir=/projects/

# 必要なファイルをローカルからコンテナにコピー
ADD requirements.txt $project_dir

# requirements.txtに記載されたパッケージをインストール                         
WORKDIR $project_dir
RUN pip install -r requirements.txt