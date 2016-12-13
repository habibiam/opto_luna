/*
 * ValveControlLib.h
 *
 *  Created on: Dec 12, 2016
 *      Author: clawton
 */

#ifndef SRC_VALVECONTROLLIB_H_
#define SRC_VALVECONTROLLIB_H_



#ifdef __cplusplus
#define BOOL bool
#else
#define BOOL int
#endif

#ifdef __cplusplus
extern "C" {
#endif


BOOL Initialize(const char *port);
void GetLastErrorMsg(char *msg, int msg_size);
int GetStatus();
BOOL SetPosition(int pos);

#ifdef __cplusplus
}
#endif




#endif /* SRC_VALVECONTROLLIB_H_ */
