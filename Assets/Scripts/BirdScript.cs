using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class BirdScript : MonoBehaviour
{
    public Rigidbody2D myrigidbody;
    public float floatstrength;
    public LogicScript logic;
    public bool birdIsAlive = true;
    
    // Start is called before the first frame update
    void Start()
    {
        // gameObject.name = "Angry Bird";
        logic = GameObject.FindGameObjectWithTag("Logic").GetComponent<LogicScript>(); 

    }
    // Update is called once per frame
    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Space) && birdIsAlive)
        {
             myrigidbody.velocity = Vector2.up * floatstrength;

        }
        if(transform.position.y>24.5||transform.position.y<-24.5)
        {
            logic.gameOver();
            birdIsAlive = false;
        }
    }
   public void OnCollisionEnter2D(Collision2D collision)
   {
    logic.gameOver();
    birdIsAlive = false;
   }
}