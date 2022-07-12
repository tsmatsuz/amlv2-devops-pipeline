# Azure Pipeline (DevOps) による MLOps Continuous Integration (AML CLI v2 による ML Pipeline 実行)

以下の手順に従ってセットアップをおこなってください。

## 事前準備

このリポジトリ サンプルは、[OpenHack の diabetes サンプルによる学習処理](https://github.com/notanaha/oh4ml-lite-diabetes) が完了していることを想定しています。<br>
特に、下記のプロビジョニングを済ませておいてください。(これらのオブジェクトを使用します。)

- Azure Machine Learning (以降、Azure ML) のワークスペースが作成済である
- Azure ML のデータアセットが、「diabetes_data_oh4ml」と「diabetes_query_oh4ml」の名前で登録済である
- Azure ML のコンピュートクラスターが、「demo-cpucluster1」の名前で作成済である
- Azure ML の環境 (environment) が、「diabetes-env-02」の名前で登録済である

## Azure Pipeline の登録

1. [Azure DevOps](https://dev.azure.com/) にログインして、新規プロジェクトを作成します。
2. 以下の手順で、このリポジトリを Azure DevOps のプロジェクトに clone します。
    - サイドメニューから "Repos" を選択します
    - "Import" ボタンを押します
    - 表示される画面の "Clone URL" に "```https://github.com/tsmatsuz/amlv2-devops-pipeline```" と入力して "Import" ボタンを押します
3. Azure DevOps から Azure に接続する際に使用する Service principal を作成します。
    - Azure ポータルにログインして、"Azure Active Dorectory" (以降、Azure AD) を選択します
    - サイドメニューから "App registrations" を選択して "New registration" ボタンを押します
    - 名前を任意に設定し、App の登録をおこないます。<br>
    なお、account type は、今回、"Accounts in this organizational directory only (Microsoft only - Single tenant)" を選択します
    - 表示される App のブレード上の "Application (client) ID" をコピーします (この ID はあとで使用します)
    - サイドメニューから "Certificate & secrets" を選択して、Client secrets を新規作成します。<br>
    作成された secret の値をコピーします (この secret の値はあとで使用します)
4. Service principal にロールを割り当てます。
    - Azure ポータル上で "Subscriptions" のブレードを表示して、利用中のサブスクリプションを選択します
    - サイドメニューの "Access control (IAM)" を選択します
    - 表示される画面上の "Add" - "Add role assignment" ボタンを選択します
    - 上記で作成した service principal に対して、Contributor (共同作成者) のロールを割り当てます
5. Azure DevOps の Pipeline で使用する Azure 接続を構成します
    - Azure DevOps のサイドメニュー下の "Project settings" を選択します
    - 表示されるメニューの "Pipelines" - "Service connections" を選択し、"Create service connection" ボタンを押します
    - 表示される画面で "Azure Resource Manager" を選択して "Next" ボタンを押します
    - 表示される認証方法の一覧から "Service principal (manual)" を選択して "Next" ボタンを押します
    - 表示される画面で以下を設定します
        - Environment : Azure Cloud
        - Scope Level : Subscription
        - Subscription Id : {AML workspace resource の存在する Azure subscription Id}
        - Subscription Name : {同 Azure subscription の名前}
        - Service Principal ID : {上記でコピーした service principal の Application ID}
        - Service Principal key : {上記でコピーした service principal の secret 値}
        - Tenant ID : {Service principal を作成した Azure AD の Tenant ID}
        - Service connection name : Azure-ARM-Dev
6. サイドメニューから "Repos" を選択して、config.yml を開き、環境にあわせて値を書き換えます (編集完了後、コミットします)。
7. サイドメニューから "Pipelines" を選択し、下記手順で Pipeline を新規作成します。
    - "Create Pipeline" ボタンを押します
    - "Where is your code?" で "Azure Repos Git" を選択します
    - "Select a repository" で、上記の clone されたリポジトリを選択します
    - "Configure your pipeline" で、"Existing Azure Pipelines YAML file" を選択します
    - 表示される画面で、上記で clone した repository 内の devops-pipelines/model-training-pipeline.yml を選択します
    - **"Run" ボタンを押さずに**、右の矢印をクリックして "Save" を選択してください (ここでは実行はおこなわず、保存のみをおこなってください)

## Azure Pipeline のトリガー実行

1. サイドメニューから "Repos" を選択し、```scripts/train-diabetes.py``` のソースコードを変更 (例えば、コメントを追加するなど) してコミットしてください。
2. ソースのコミットをトリガーとして、上記で登録した Azure Pipeline が実行 (Run) されます。
3. 終了後、Azure ML 上でモデル「diabetes_model_oh4ml」が登録されていることを確認します。

> Note : Event Grid を用いて Azure Machine Learning 上のさまざまなトリガーに応じた処理を構築できます。(詳細は [こちら](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-event-grid) を参照)
