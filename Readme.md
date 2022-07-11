# Model 登録のトリガーによる Azure Pipeline 実行 (AML CLI v2 による Model のデプロイ)

## Azure Pipeline の登録

1. [Azure DevOps](https://dev.azure.com/) にログインして、新規プロジェクトを作成、このリポジトリを clone します。
    - サイドメニューから "Repos" を選択します
    - "Import" ボタンを押します
    - 表示される画面で、"Clone URL" に "https://github.com/tsmatsuz/amlv2-devops-pipeline" と入力して "Import" ボタンを押します
2. Azure DevOps から Azure に接続する際に使用する Service principal を作成します。
    - Azure にログインして、"Azure Active Dorectory" を選択します
    - サイドメニューから "App registrations" を選択して "New registration" ボタンを押します
    - 名前を適宜設定して、App の登録をおこないます。<br>
    なお、account type は "Accounts in this organizational directory only (Microsoft only - Single tenant)" を選択します
    - 表示される App のブレード上の "Application (client) ID" をコピーします (この ID は、あとで使用します)
    - サイドメニューから "Certificate & secrets" を選択して、Client secrets を新規作成します。<br>
    作成された secret の値をコピーします (secret は、あとで使用します)
3. Service principal にロールを割り当てます。
    - Azure ポータル上で "Subscription" のブレードを表示します
    - サイドメニューの "Access control (IAM)" を選択します
    - "Add" - "Add role assignment" を選択します
    - 上記で作成した service principal に対して、Contributor (共同作成者) のロールを割り当てます
4. Azure DevOps の Pipeline で Azure 接続を構成します
    - Azure DevOps のサイドメニュー下の "Project settings" を選択します
    - 表示されるメニューの "Pipelines" - "Service connections" を選択し、"Create service connection" ボタンを押します
    - 表示される画面で "Azure Resource Manager" を選択して "Next" ボタンを押します
    - 表示される認証方法の一覧から "Service principal (manual)" を選択して "Next" ボタンを押します
    - 表示される画面で以下を設定します
        - Environment : Azure Cloud
        - Scope Level : Subscription
        - Subscription Id : {AML resource の存在する Azure subscription Id}
        - Subscription Name : {Azure subscriptoin の名前}
        - Service Principal ID : {上記でコピーした service principal の Application ID}
        - Service Principal key : {上記でコピーした service principal の secret 値}
        - Tenant ID : {Service principal を作成した Azure AD の Tenant ID}
        - Service connection name : Azure-ARM-Dev
5. サイドメニューから "Repos" を選択し、config.yml を開いて、必要な値に書き換えます
6. サイドメニューから "Pipelines" を選択し、下記手順で Pipeline を定義します。
    - "Create Pipeline" ボタンを押します
    - "Where is your code?" で "Azure Repos Git" を選択します
    - "Select a repository" で、上記の clone したコードが入ったプロジェクトを選択します
    - "Configure your pipeline" で、"Existing Azure Pipelines YAML file" を選択します
    - 表示される画面で、上記で clone した repository 内の devops-pipelines/deploy-online-endpoint-pipeline.yml を選択します
    - "Run" ボタンの右の矢印をクリックして "Save" を選択してください (ここでは実行はおこなわず、保存のみをおこないます)
