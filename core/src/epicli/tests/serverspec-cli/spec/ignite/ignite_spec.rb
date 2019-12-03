require 'spec_helper'

$ignite_rest_api_host = '127.0.0.1'
$ignite_rest_api_port = 8080
$ignite_jdbc_port = 10800
$cacheName = 'epi-test'

def checkAPIconnection
  describe 'Checking API connection' do
    describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=version'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def createCache
  describe 'Checking if it is possible to create a cache' do
    describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=getorcreate&cacheName=#{$cacheName}'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def addKeyValuePairs
    describe 'Checking if it is possible to add key-value pairs to cache' do
      describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=putall&k1=testKey1&k2=testKey2&k3=testKey3&v1=testValue1&v2=testValue2&v3=testValue3&cacheName=#{$cacheName}'") do
        its(:stdout_as_json) { should include('successStatus' => 0) }
        its(:exit_status) { should eq 0 }
      end
    end
end

def getKeyValuePairs
  describe 'Checking if it is possible to get values mapped to the specified keys from cache' do
    describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=getall&k1=testKey1&k2=testKey2&k3=testKey3&cacheName=#{$cacheName}'") do
      its(:stdout_as_json) { should include('response' => include('testKey1' => 'testValue1')) }
      its(:stdout_as_json) { should include('response' => include('testKey2' => 'testValue2')) }
      its(:stdout_as_json) { should include('response' => include('testKey3' => 'testValue3')) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def getCacheSize
  describe 'Checking if it is possible to get the number of all entries cached across all nodes' do
    describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=size&cacheName=#{$cacheName}'") do
      its(:stdout_as_json) { should include('response' => 3) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def destroyCache
  describe 'Checking if it is possible to destroy a cache' do
    describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=destcache&cacheName=#{$cacheName}'") do
      its(:stdout_as_json) { should include('successStatus' => 0) }
      its(:exit_status) { should eq 0 }
    end
  end
end

def checkJDBCconnection
  describe 'Checking JDBC connection' do
    describe command("echo \"SELECT 2 + 2 * 2 as RESULT ;\" | /opt/ignite/bin/sqlline.sh -u jdbc:ignite:thin://127.0.0.1/") do
      its(:stdout) { should match /\b6\b/ }    
      its(:exit_status) { should eq 0 }
    end
  end
end

def createTable
  describe 'Checking if it is possible to create a test table' do
    describe command("echo \"CREATE TABLE EPI_TEST_TABLE (id int, name varchar, PRIMARY KEY (id)) WITH \\\"CACHE_NAME=#{$cacheName}-ddl\\\";\" | /opt/ignite/bin/sqlline.sh -u jdbc:ignite:thin://127.0.0.1/ 2>&1") do
      its(:stdout) { should match /No rows affected/ }
      its(:stdout) { should_not match /Error/ }    
      its(:exit_status) { should eq 0 }
    end
  end
end

def insertValuesIntoTable
  describe 'Checking if it is possible to insert values into the test table' do
    describe command("echo \"INSERT INTO EPI_TEST_TABLE(id, name) values (1, 'SUCCESS');\" | /opt/ignite/bin/sqlline.sh -u jdbc:ignite:thin://127.0.0.1/ 2>&1") do
      its(:stdout) { should match /1 row affected/ }
      its(:stdout) { should_not match /Error/ }    
      its(:exit_status) { should eq 0 }
    end
  end
end

def selectValuesFromTable
  describe 'Checking if it is possible to select values from the test table' do
    describe command("echo \"SELECT id, name FROM EPI_TEST_TABLE;\" | /opt/ignite/bin/sqlline.sh -u jdbc:ignite:thin://127.0.0.1/ 2>&1") do
      its(:stdout) { should match /1 row selected/ }
      its(:stdout) { should match /SUCCESS/ }
      its(:stdout) { should_not match /Error/ }    
      its(:exit_status) { should eq 0 }
    end
  end
end

def getValueFromTableViaAPI
  describe 'Checking if it is possible to get values from table created with DDL statement ' do
    describe command("curl 'http://#{$ignite_rest_api_host}:#{$ignite_rest_api_port}/ignite?cmd=qryfldexe&pageSize=10&cacheName=#{$cacheName}-ddl&qry=select+name+from+EPI_TEST_TABLE' | jq '.response.items'") do
      its(:stdout) { should match /\bSUCCESS\b/ }
      its(:exit_status) { should eq 0 }
    end
  end
end

def dropTable
  describe 'Checking if it is possible to drop the test table' do
    describe command("echo \"DROP TABLE IF EXISTS EPI_TEST_TABLE;\" | /opt/ignite/bin/sqlline.sh -u jdbc:ignite:thin://127.0.0.1/ 2>&1") do
      its(:stdout) { should match /No rows affected/ }
      its(:stdout) { should_not match /Error/ }    
      its(:exit_status) { should eq 0 }
    end
  end
end  

describe 'Checking if Ignite service is running' do
  describe service('ignite') do
    it { should be_enabled }
    it { should be_running }
  end
end

describe 'Checking if the ports are open' do
  let(:disable_sudo) { false }
  describe port($ignite_jdbc_port) do
    it { should be_listening }
  end
  describe port($ignite_rest_api_port) do
    it { should be_listening }
  end
end 

nodes =  listInventoryHosts("ignite")

checkAPIconnection
checkJDBCconnection

if nodes[0].include? host_inventory['hostname']
  createCache
  addKeyValuePairs
  createTable
  insertValuesIntoTable
end

getKeyValuePairs
getCacheSize
selectValuesFromTable
getValueFromTableViaAPI

if nodes[nodes.length-1].include? host_inventory['hostname']
  destroyCache
  dropTable
end
