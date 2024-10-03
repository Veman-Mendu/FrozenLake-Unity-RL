using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using AustinHarris.JsonRpc;
using System.Linq;

public class BoxAgent : MonoBehaviour
{

    class Rpc : JsonRpcService
    {
        BoxAgent agent;

        public Rpc(BoxAgent agent)
        {
            this.agent = agent;
        }

        [JsonRpcMethod]
        void sendTest(string message)
        {
            Debug.Log($"Message Recieved is : {message}");
        } 

        [JsonRpcMethod]
        string recieveTest()
        {
            return "Hello Python";
        }

        //Below are the methods related to the RL training
        [JsonRpcMethod]
        string resetGame()
        {
            return agent.Reset();
        }

        [JsonRpcMethod]
        string takeAction(int action)
        {
            return agent.Action(action);
        }
    }

    Rpc rpc;
    // Start is called before the first frame update
    void Start()
    {
        rpc = new Rpc(this);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    //Let's Reset the Game here
    public GameObject target;
    public GameObject lake1, lake2, lake3, lake4;
    public int holeLayer;
    public Material holeMaterial;
    public string Reset()
    {
        
        //Fix the agent and target initial positions
        int agentX = 0;
        int agentZ = 6;

        int targetX = 6;
        int targetZ = 0;

        //Keep the agent from moving by zeroing both linear and angular momentum of the agent
        this.gameObject.GetComponent<Rigidbody>().angularVelocity = this.gameObject.GetComponent<Rigidbody>().velocity = Vector3.zero;

        //Let's mark the initial position of the agent and target on the lake
        this.gameObject.transform.localPosition = new Vector3(agentX, 0.41f, agentZ);
        this.gameObject.transform.rotation = Quaternion.Euler(new Vector3(0,0,0));
        target.transform.localPosition = new Vector3(targetX, 0.41f, targetZ);

        //Make sure the lake blocks are set to lake for rendering when the episode begins
        lake1.layer = lake2.layer = lake3.layer = lake4.layer = holeLayer;
        lake1.GetComponent<Renderer>().material = lake2.GetComponent<Renderer>().material = lake3.GetComponent<Renderer>().material = lake4.GetComponent<Renderer>().material = holeMaterial;

        int agentPos = agentX*4 + agentZ;
        return $"agentX:{agentX}, agentZ:{agentZ}, agentPos:{agentPos}";
    }

    public float moveSpeed;

    public string Action(int action)
    {
        switch (action)
        {
            case 0:
                this.gameObject.transform.position += new Vector3(0,0,2);
                //this.gameObject.GetComponent<Rigidbody>().MovePosition(this.gameObject.transform.position + new Vector3(0,0,2));
                break;
            case 1:
                //this.gameObject.GetComponent<Rigidbody>().MovePosition(this.gameObject.transform.position + new Vector3(2,0,0));
                this.gameObject.transform.position += new Vector3(2,0,0);
                break;
            case 2:
                //this.gameObject.GetComponent<Rigidbody>().MovePosition(this.gameObject.transform.position + new Vector3(0,0,-2));
                this.gameObject.transform.position += new Vector3(0,0,-2);
                break;
            case 3:
                //this.gameObject.GetComponent<Rigidbody>().MovePosition(this.gameObject.transform.position + new Vector3(-2,0,0));
                this.gameObject.transform.position += new Vector3(-2,0,0);
                break;
            default:
                break;
        }

        if (Mathf.Abs(this.gameObject.transform.position.x) < 0.0001f)
        {
            this.gameObject.transform.position = new Vector3(0,this.gameObject.transform.position.y,this.gameObject.transform.position.z);
        }

        if (Mathf.Abs(this.gameObject.transform.position.z) < 0.001f)
        {
            this.gameObject.transform.position = new Vector3(this.gameObject.transform.position.x, this.gameObject.transform.position.y, 0);
        }

        float agentPos = this.gameObject.transform.position.x * 4 + this.gameObject.transform.position.z;
        float targetPos = target.transform.position.x * 4 + target.transform.position.z;
        int reward = GetReward(this.gameObject.transform.position.x, this.gameObject.transform.position.z, targetPos);
        int done = 0;

        switch (reward)
        {
            case 1:
                done = 1;
                break;
            case -1:
                done = 1;
                break;
            case 0:
                done = 0;
                break;
            default:
                break;
        }
        
        return $"observation:{agentPos}, reward:{reward}, done:{done}, agentX:{this.gameObject.transform.position.x}, agentZ:{this.gameObject.transform.position.z}";
    }

    public int GetReward(float agentX, float agentZ, float targetPos)
    {
        float agentPos = agentX * 4 + agentZ;
        int reward;
        List<float> states = new List<float> {12,28,26,0};
        List<float> array_num = new List<float> {0,2,4,6};

        if ((array_num.Contains(agentX)) && (array_num.Contains(agentZ)))
        {
            Debug.Log($"Agent in the game {agentX}, {agentZ}");
            if (states.Contains(agentPos))
            {
                Debug.Log($"Agent in the lake");
                reward = -1;
            }
            else if (agentPos == targetPos)
            {
                Debug.Log($"Agent reached the target");
                reward = 1;
            }
            else
            {
                Debug.Log($"Agent still playing");
                reward = 0;
            }
        }
        else
        {
            Debug.Log($"{agentX}, {array_num.Contains(agentX)}, {array_num.Contains(agentZ)}");
            reward = -1;
        }

        return reward;
    }
}
